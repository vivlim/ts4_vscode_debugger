# patch over vis text because it crashes.
import sims4
from vivlib2.idempotent_exec import idempotent_exec
from vivlib2.messagebox import CatchAndMsgBox
import vivlib2.main_thread
import pathlib,sys

# hook the core_services.on_tick function so that we can be called periodically (frequently) and have an opportunity to run code on main thread
main_thread = vivlib2.main_thread.MainThreadDispatcher()

if pathlib.Path(sys.executable).name.casefold() == "TS4_x64.exe".casefold():
    import sims4.core_services
    sims4.core_services.on_tick = main_thread.wrap_on_tick(sims4.core_services.on_tick)

def block_debugvis_text():
    import debugvis,sims4
    orig_get_layer = debugvis.get_layer
    class WrappedLayer:
        def __init__(self, l):
            self.l = l
        def open(self):
            self.l.open()
        def clear(self):
            self.l.clear()
        def commit(self):
            self.l.commit()
        def add_segment(self, a, b, color):
            self.l.add_segment(a, b, color)
        def add_point(self, a, b, color):
            self.l.add_point(a, b, color)  
        def add_text_screen(self, *args, **kwargs):
            pass
        def add_text_world(self, *args, **kwargs):
            pass
        def add_text_object(self, *args, **kwargs):
            pass

    def get_wrapped_layer(*args, **kwargs):
        l = orig_get_layer(*args, **kwargs)
        wl = WrappedLayer(l)
        return wl
    debugvis.get_layer = get_wrapped_layer

    OrigContext = debugvis.Context
    class WrappedContext(OrigContext):
        def __init__(self, name, preserve=False, color=sims4.color.Color.WHITE, altitude=0.05, zone_id=None, routing_surface=None):
            OrigContext.__init__(self, name, preserve, color, altitude, zone_id, routing_surface)
            self.layer = WrappedLayer(self.layer)
    debugvis.Context = WrappedContext

    def _undo():
        debugvis.get_layer = orig_get_layer
        debugvis.Context = OrigContext
        return True

    return _undo

# idempotent_exec("block_debugvis_text", block_debugvis_text)
block_debugvis_text()


# def __vivexec():
#   import services
# #   account = services.account_service().get_current_account()
# #   household_id = services.owning_household_id_of_active_lot()
# #   stash['account']=account
# #   stash['household_id']=household_id
# #   p(f"account {account}, household_id {household_id}")
# #   client = services.client_manager().create_client(696968, account, household_id)
#   client = services.get_first_client()
#   stash['client']=client
#   p(f"obtained client: {client}")
  
#   session_id = client.id # steal this
#   name="idklol2"
  
#   #client = services.client_manager().get(_connection) # already have from above
#   import sims4,math,services,types
#   from sims4.color import Color, pseudo_random_color
#   from debugvis import Context
#   import objects.components.types
#   from visualization.sim_position_visualizer import SimPositionVisualizer
  
#   object_manager = services.object_manager()
#   if object_manager is None:
#     return False
#   else:
#     for obj in object_manager.get_all_objects_with_component_gen(objects.components.types.ROUTING_COMPONENT):
#       routing_component = obj.routing_component
#       if routing_component is None:
#         pass
#       else:
#         layer = '{0}_{1:08x}'.format('sim_pos', obj.id)
#         visualizer = SimPositionVisualizer(obj, layer)
# #         _sim_layer_visualizers[obj.id] = visualizer
#         sims4.commands.output('Added visualization: {0}'.format(layer), session_id)
#         p(f"Enable layer {layer}")
#         sims4.commands.client_cheat('debugvis.layer.enable {0}'.format(layer), session_id)

# if 'wrapped_layer' in globals():
#   main_run(__vivexec)