hg close

With this extension, you can close branches in Mercurial without `hg
update` to the specific branch. This makes branch closing fast and
efficient.

You can grab the code as follows. I have a dedicated `.hgext` folder
for all of my Mercurial extensions.
```
git clone http://github.pal.us.bosch.com/MAC1PAL/close-branch.git
```

Add the following line to the `[extensions]` section of your `hgrc`
```
close = ~/.hgext/close-branch/close-branch.py'
```

Then, you perform commands like this:
```
hg close stupid-branch -m "Closing branch"
```