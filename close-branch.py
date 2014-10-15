#!/usr/bin/env python

'''

'''

from mercurial import commands, scmutil, util

def getchangecontext(ui, repo, rev):

    ctx = scmutil.revsingle(repo, rev)

    return ctx

def close(ui, repo, branch=None, **opts):

    # check repository
    if not repo:
        raise util.Abort(_("there is no Mercurial repository here "
                           "(.hg not found)"))
    # check for a branch
    if not branch:
        raise util.Abort('no branch provided')

    # check message
    m = opts.get('message')
    if not m:
        raise util.Abort('empty commit message')

    # get current context
    originalctx = repo[None]
    
    # get branch change context
    branchctx = getchangecontext(ui, repo, branch)
        
    # move to other node and branch
    commands.debugsetparents(ui, repo, branchctx.rev())
    commands.branch(ui, repo, label=branchctx.branch())

    # commit close node
    commands.commit(ui, repo, close_branch=True, message=m, exclude="*")
        
    # switch back to original
    commands.debugsetparents(ui, repo, originalctx.rev())
    commands.branch(ui, repo, label=originalctx.branch())


cmdtable = {
    "close":
        (close, [
            ('m', 'message', '', 'use text as commit message')
            ],
         'hg close BRANCH')
}
