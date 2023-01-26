# add bin folder to r-path
# https://nixos.org/patchelf.html
# https://stackoverflow.com/questions/39978762/linux-executable-cant-find-shared-library-in-same-folder
patchelf --set-rpath '${ORIGIN}' libaudresample.so
