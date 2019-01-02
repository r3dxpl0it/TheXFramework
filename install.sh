echo "......................................................"
echo "THE X FRAMWORK INSTALLER"
echo "UPDATING AND INSTALLING LIBRARIES, MODULES AND DEPENDENCIES"
echo "......................................................"
echo ""
echo "......................................................"
echo "Updating"
echo "......................................................"
sudo apt-get update 
echo "......................................................"
echo "Upgrading"
echo "......................................................"
sudo apt-get upgrade
echo "......................................................"
echo "Installing Libraries"
echo "......................................................"
sudo apt-get install libxml2 libxslt libxml
sudo apt-get install python python-dev python-all python-all-dev python3 
sudo apt-get install python3-dev python3-pip libxslt1-dev libxml2-dev python3 zlib1g-dev
echo "......................................................"
echo "Installing Modules"
echo "......................................................"
sudo apt-get install nmap golismero sqlmap nikto 
echo "......................................................"
echo "Installing Python2 Modules" 
echo "......................................................"
pip install -r requirements.txt
echo "......................................................"
echo "Installing Python3 Modules" 
echo "......................................................"
pip3 install -r requirements_3.txt
