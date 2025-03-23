
import sims4.commands
@sims4.commands.Command('inspect.world', command_type=sims4.commands.CommandType.Live)
def inspect_world(_connection=None):
    import vivlib2.main_thread # hook main thread so we can dispatch to it from a background thread.
    
    output = sims4.commands.CheatOutput(_connection)
    import vivlib2.draw
    try:
        output("starting coordinate inspector...")
        vivlib2.draw.start_draw_pick_locations()
        output("ok!")
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        output(f"Failed to start coordinate inspector: {tb}")