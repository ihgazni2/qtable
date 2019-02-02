pip3 uninstall qtable
git rm -r dist
git rm -r build
git rm -r qtable.egg-info
rm -r dist
rm -r build
rm -r qtable.egg-info
git add .
git commit -m "remove old build"
