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


import typing.NamedTuple
class XZ(typing.NamedTuple):
    x: int
    z: int

class Bounds(typing.NamedTuple):
    min: XZ
    max: XZ

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
