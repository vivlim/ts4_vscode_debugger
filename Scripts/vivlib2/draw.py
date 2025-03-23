import vivlib2

class DrawLayer:
    def __init__(self, name, enabled=True):
        import vivlib2.main_thread
        self.name = name
        self.main_thread = vivlib2.main_thread.MainThreadDispatcher()
        if enabled:
            self.client_enable()
    
    def _exec_client_cmd(self, cmd):
        @vivlib2.log_exception_and_raise
        def _exec_on_main_thread():
            import services,sims4
            client = services.get_first_client()
            sims4.commands.client_cheat(cmd, client.id)
        self.main_thread.run_on_main_thread(_exec_on_main_thread)

    def client_enable(self):
        self._exec_client_cmd('debugvis.layer.enable {0}'.format(self.name))

    def client_disable(self):
        self._exec_client_cmd('debugvis.layer.disable {0}'.format(self.name))

    def draw_in_context(self, drawfn):
        @vivlib2.log_exception_and_raise
        def _exec_on_main_thread():
            import debugvis
            with debugvis.Context(self.name) as layer:
                drawfn(layer)
        self.main_thread.run_on_main_thread(_exec_on_main_thread)


import typing
class XZ(typing.NamedTuple):
    x: int
    z: int

class Bounds(typing.NamedTuple):
    min: XZ
    max: XZ


# example
# g = Grid(Bounds(XZ(0, 0), XZ(1000, 1000)), 20)
# g.draw(dl3)
class Grid:
    def __init__(self, bounds: Bounds, step: float):
        self.bounds = bounds
        self.step = step
    
    def draw(self, drawlayer: DrawLayer):

        @vivlib2.log_exception_and_raise
        def drawfn(layer):
            from sims4.math import Vector3
            import services, routing
            terrain_object = services.terrain_service.terrain_object()
            routing_surface = routing.SurfaceIdentifier(services.current_zone_id(), 0, routing.SurfaceType.SURFACETYPE_WORLD)

            for x in range(self.bounds.min.x, self.bounds.max.x, self.step):
                for z in range(self.bounds.min.z, self.bounds.max.z, self.step):
                    y = terrain_object.get_routing_surface_height_at(x, z, routing_surface)
                    point = Vector3(x, y, z)
                    layer.add_point(point, routing_surface=None)

        drawlayer.draw_in_context(drawfn)
    

@vivlib2.lazy_global
def get_last_pick_location():
    import sims4.math
    return sims4.math.Vector3(0,0,0)

@vivlib2.lazy_global
def get_last_pick_location_drawlayer():
    return DrawLayer("pick")

@vivlib2.lazy_global
def get_last_pick_queue():
    import queue
    return queue.Queue(64)

# factor this out so it's easy to monkeypatch & iterate on visuals
def draw_pick_at_location(drawlayer: DrawLayer, location):
    import vivlib2.line_writer
    
    def drawpick(layer):
        from sims4.math import Vector3
        arrow_start = location + Vector3(0, 2, 0)
        layer.add_point(location)
        layer.add_point(arrow_start)
        layer.add_segment_absolute(location, arrow_start)
        lw = vivlib2.line_writer.LineWriter(arrow_start, 0.2, 'x{:.2f}\ny{:.2f}\nz{:.2f}'.format(location.x, location.y, location.z))
        lw.write(layer)
    drawlayer.draw_in_context(drawpick)

def start_draw_pick_locations():
    import world.pick_tests
    #world.pick_tests.PickTerrainTest.__call__ = orig
    pick_drawlayer = get_last_pick_location_drawlayer()

    import vivlib2
    import vivlib2.queues

    @vivlib2.log_exception
    def draw_pick_location_if_changed(pick_location):
        lpl = get_last_pick_location()
        if pick_location.x != lpl.x or pick_location.y != lpl.y or pick_location.z != lpl.z:
            vivlib2.get_logger().info(f"pick location changed: {pick_location}")
            # p(f"pick location changed {pick_location}\n")
            lpl.x = pick_location.x
            lpl.y = pick_location.y
            lpl.z = pick_location.z
            draw_pick_at_location(pick_drawlayer, pick_location)
    vivlib2.queues.service_queue_on_thread(get_last_pick_queue(), draw_pick_location_if_changed)

    last_pick_queue = get_last_pick_queue()
    orig = world.pick_tests.PickTerrainTest.__call__

    def replacement_pick_terrain_test_call(*args, **kwargs):
        try:
            if 'context' in kwargs:
                context = kwargs['context']
                last_pick_queue.put_nowait(context.pick.location)
        except:
            pass

        return orig(*args, **kwargs)
    world.pick_tests.PickTerrainTest.__call__ = replacement_pick_terrain_test_call