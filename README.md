# Narwhallet - alpha
## **UN-Official** Kevacoin ElectrumX Wallet

# Runable version see 'qt' branch. This branch undergoing change and not yet useable.

### Please Note
This project currently in **alpha**.

That means this is a **work-in-progress**. While in alpha project will be undergoing large amounts of cleanup and refactors.

Please proceed with caution because things probably will be a bit unstable. If a crash or other unintended result does occur, please report it so it can be addressed!

Until initial beta release recommended to use a read-only or watch wallet.


## Setup Ubuntu
You will need Python and Git installed, can install both via apt with the command:<br/>
sudo apt install python3 git<br/>

### venv example
*recommended to use a virtual environment for separation and to ensure no dependency conflicts*<br/>
mkdir K1<br/>
cd K1<br/>
python3 -m venv ./venv<br/>
source ./venv/bin/activate<br/>

### Download repo & Install requirements
git clone https://github.com/kevaone/narwhallet.git<br/>
cd narwhallet<br/>
pip install -r ./requirements.txt<br/>

### Pango support
pip uninstall kivy<br/>
mkdir kivy-deps-build && cd kivy-deps-build<br/>
curl https://raw.githubusercontent.com/kivy/kivy/master/tools/build_linux_dependencies.sh -o build_kivy_deps.sh<br/>
chmod +x build_kivy_deps.sh<br/>
./build_kivy_deps.sh<br/>
export KIVY_DEPS_ROOT=$(pwd)/kivy-dependencies<br/>
export USE_PANGOFT2=1<br/>
export KIVY_TEXT='pango'<br/>
pip install --no-binary :all: kivy<br/>

### Launch
python3 ./main.py<br/>

### (optional) Build
pip install pyinstaller<br/>
cd share<br/>
pyinstaller linux_gui_with_deps.spec<br/>
cd dist<br/>
./Narwhallet<br/>

### (optional) Android Build
pip install buildozer<br/>
We also need older version of Cython; we can just use pip and install from wheel:<br/>
pip install https://github.com/cython/cython/releases/download/0.29.33/Cython-0.29.33-py2.py3-none-any.whl<br/>
buildozer android release<br/>


## Setup Windows
You will need Python installed, can download and install from https://www.python.org/downloads/windows/. You will also need Git which can be downloaded and installed from https://git-scm.com/download/win.<br/>

You can test the instilation status by opening a command prompt and issuing the commands:<br/>
<br/>
python --version<br/>
git --version<br/>
<br/>
If either of these commands fail check the instilation status of the program. If the program is installed it might not be added to PATH; consult the programs documentation on how to add.<br/>

### venv example
*recommended to use a virtual environment for separation and to ensure no dependency conflicts*<br/>
mkdir K1<br/>
cd K1<br/>
python -m venv .\venv<br/>
.\venv\Scripts\activate<br/>

### Download repo & Install requirements
git clone https://github.com/kevaone/narwhallet.git<br/>
cd narwhallet<br/>
pip install -r ./requirements.txt<br/>

### Launch
python3 ./main.py<br/>

### (optional) Build
pip install pyinstaller pillow<br/>
cd share<br/>
pyinstaller linux_gui_with_deps.spec<br/>
cd dist<br/>
Narwhallet.exe<br/>

### (optional) Android Build
pip install buildozer<br/>
Also enable Windows Subsystem for Linux (WSL) and install a Linux distribution: https://docs.microsoft.com/en-us/windows/wsl/install to use buildozer with Windows<br/>
We also need older version of Cython; we can just use pip and install from wheel:<br/>
pip install https://github.com/cython/cython/releases/download/0.29.33/Cython-0.29.33-py2.py3-none-any.whl<br/>
buildozer android release<br/>

**Upon launch Narwhallet will create the directory .narwhalllet within you're home directory. You're wallets, address book, settings and cache are saved here.**

It is also highly recommended you run your own instance of ElectrumX. If you have large wallets or large number of wallets you will probably be throttled updating against public peers; Running your own ElectrumX you can adjust for your needs.

Can download ElectrumX here: https://github.com/kevacoin-team/electrumx


## Wallets Supported

### Normal Wallets
Create or restore bip32/bip49 based wallets

### Read Only Wallet
Restore an ypub or track wallet addresses

### Watch Wallet
Track individual addresses

**Important Notes**
While experimenting with alpha perform initial sych with the default peer unless running your own. Initial tx/ns cache building will be getting refined further to reduce calls and load to allow faster synch.
