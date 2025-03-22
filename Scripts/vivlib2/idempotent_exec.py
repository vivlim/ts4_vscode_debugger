from vivlib2.messagebox import CatchAndMsgBox

# runs a function once - that function can return an undoing function, and future invocations will revert
# revertfn should return True if the function can be safely run again
@CatchAndMsgBox('idempotent_exec')
def idempotent_exec(key, f):
    if not 'idempotent_exec_state' in globals():
        globals()['idempotent_exec_state'] = {}
    if key in globals()['idempotent_exec_state']:
        revertfn = globals()['idempotent_exec_state']
        can_run_again = revertfn()

        if can_run_again:
            del globals()['idempotent_exec_state'][key]

    if not key in globals()['idempotent_exec_state']:
        undofn = f()
        if undofn is None:
            def no_undo():
               pass
            undofn = no_undo
        globals()['idempotent_exec_state'][key] = undofn
