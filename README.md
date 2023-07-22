# Narwhallet - alpha
## **UN-Official** Kevacoin ElectrumX Wallet

# Runable version see 'qt' branch. This branch undergoing change and not yet useable.

### Please Note
This project currently in **alpha**.

That means this is a **work-in-progress**. While in alpha project will be undergoing large amounts of cleanup and refactors.

Please proceed with caution because things probably will be a bit unstable. If a crash or other unintended result does occur, please report it so it can be addressed!

Until initial beta release recommended to use a read-only or watch wallet.


## Setup Ubuntu
*recommended to use a virtual environment for separation and to ensure no dependency conflicts*

### venv example
mkdir K1<br/>
cd K1<br/>
python3 -m venv ./venv<br/>
source ./venv/bin/activate<br/>

### Download repo & Install requirements
git clone https://github.com/kevaone/narwhallet.git<br/>
cd narwhallet<br/>
pip install -r ./requirements.txt<br/>

### Launch
python3 ./narwhallet_gui.py<br/>

### (optional) Build
pip install pyinstaller<br/>
cd share<br/>
pyinstaller linux_gui_with_deps.spec<br/>
cd dist<br/>
./Narwhallet<br/>

## Setup Windows
*recommended to use a virtual environment for separation and to ensure no dependency conflicts*

### venv example
mkdir K1<br/>
cd K1<br/>
python -m venv ./venv<br/>
.\venv\Scripts\activate<br/>

### Download repo & Install requirements
git clone https://github.com/kevaone/narwhallet.git<br/>
cd narwhallet<br/>
pip install -r ./requirements.txt<br/>

### Launch
python3 ./narwhallet_gui.py<br/>

### (optional) Build
pip install pyinstaller<br/>
cd share<br/>
pyinstaller linux_gui_with_deps.spec<br/>
cd dist<br/>
Narwhallet.exe<br/>

**Upon launch Narwhallet will create the directory .narwhalllet within you're home directory. You're wallets, address book, settings and cache are saved here.**

It is also highly recommended you run your own instance of ElectrumX. If you have large wallets or large number of wallets you will probably be throttled updating against public peers; Running your own ElectrumX you can adjust for your needs.

Can download ElectrumX here: https://github.com/kevacoin-team/electrumx


## Wallets Supported

### Normal Wallets
Create or restore mnemonic phrase for bip49 based wallet

### Read Only Wallet
Restore an ypub or track wallet addresses

### Watch Wallet
Track individual addresses

**Important Notes**
While experimenting with alpha perform initial sych with the default peer unless running your own. Initial tx/ns cache building will be getting refined further to reduce calls and load to allow faster synch.
