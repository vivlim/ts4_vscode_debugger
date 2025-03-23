
import sims4.commands
@sims4.commands.Command('inspect.world', command_type=sims4.commands.CommandType.Live)
def inspect_world(_connection=None):
    import vivlib2.main_thread # hook main thread so we can dispatch to it from a background thread.
    
    output = sims4.commands.CheatOutput(_connection)
    import vivlib2.draw
    from vivlib2.draw import Grid, Bounds, XZ
    import vivlib2.line_writer # dependency not used directly, but we want to pack it
    import vivlib2

    @vivlib2.lazy_global
    def init_once():
        try:
            vivlib2.hollow_logger().add_callback(output)
            output("adding grid...")
            grid = vivlib2.draw.Grid(Bounds(XZ(0, 0), XZ(1000, 1000)), 3)
            grid_layer = vivlib2.draw.DrawLayer("grid")
            grid.draw(grid_layer)
            output("grid ok!")
            
            output("starting coordinate inspector...")
            vivlib2.draw.start_draw_pick_locations()
            output("coordinate inspector ok! coordinates will be shown after clicking on the ground.")
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            output(f"Failed to start: {tb}")

    init_once()