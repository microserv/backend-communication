echo "Installing dependencies..."
sudo apt-get install libncurses5-dev libreadline-dev nettle-dev libgnutls28-dev build-essential cmake
sudo apt-get install cython3 python3-dev python3-setuptools

### Install msgpack-c 1.3 ###
echo "Installing msgpack..."
wget https://github.com/msgpack/msgpack-c/releases/download/cpp-1.3.0/msgpack-1.3.0.tar.gz
tar -xzf msgpack-1.3.0.tar.gz
cd msgpack-1.3.0 && mkdir build && cd build
cmake -DMSGPACK_CXX11=ON -DMSGPACK_BUILD_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX=/usr ..
make -j
sudo make install


### Install openhdt ###
echo "Installing opendht"
git clone https://github.com/savoirfairelinux/opendht.git

# build and install
cd opendht
mkdir build && cd build
cmake -DOPENDHT_PYTHON=ON -DCMAKE_INSTALL_PREFIX=/usr ..
make -j
sudo make install
