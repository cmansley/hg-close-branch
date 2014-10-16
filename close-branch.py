#!/usr/bin/env python

'''close a branch without updating to the branch

Quickly close branches all over the repository without incurring the
penalty of updating to the branch.
'''
from mercurial import commands, scmutil, util

def close(ui, repo, branch=None, **opts):
    '''close a branch without updating to the branch
    
    Takes a branch and closes it with a commit message.

    This is extremely helpful in large repositories, where updating to
    different branches can take seconds.
    '''
    # check repository
    if not repo:
        raise util.Abort(_("there is no Mercurial repository here "
                           "(.hg not found)"))
    # check for a branch
    if not branch:
        raise util.Abort('no branch provided')

    # get message
    m = opts.get('message')

    # get current context
    originalctx = repo[None]

    # the current working directory might have two parents (merge scenario)
    # check for a single parent and then pick correct parent
    if len(originalctx.parents()) != 1:
        raise util.Abort('current directory has an outstanding merge')
    originalctx = originalctx.parents()[0]
    
    # get branch change context
    branchctx = scmutil.revsingle(repo, branch)
        
    # move to other node and branch
    commands.debugsetparents(ui, repo, branchctx.rev())
    old_quiet = ui.quiet
    ui.quiet = True
    commands.branch(ui, repo, label=branchctx.branch())
    ui.quiet = old_quiet

    # commit close node
    commands.commit(ui, repo, close_branch=True, message=m, exclude="*")
        
    # switch back to original
    commands.debugsetparents(ui, repo, originalctx.rev())
    old_quiet = ui.quiet
    ui.quiet = True
    commands.branch(ui, repo, label=originalctx.branch())
    ui.quiet = old_quiet


cmdtable = {
    "close":
        (close, [
            ('m', 'message', '', 'use text as commit message')
            ],
         'hg close BRANCH')
}
