pyrcc5 -o unity8b_rc.py unity8b.qrc
call nuitka --show-progress --show-modules --standalone --windows-disable-console --nofreeze-stdlib --recurse-to=augur --python-flag=no_site unity8b.py
if not %errorlevel%==0 goto:error
call robocopy /S build unity8b.dist
goto:exit
:error
echo Error!
:exit
