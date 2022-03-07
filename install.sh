#  __  __    _  _____ ____  _____  __     _    ____  __  __ ___ _   _ 
# |  \/  |  / \|_   _|  _ \|_ _\ \/ /    / \  |  _ \|  \/  |_ _| \ | |
# | |\/| | / _ \ | | | |_) || | \  /    / _ \ | | | | |\/| || ||  \| |
# | |  | |/ ___ \| | |  _ < | | /  \   / ___ \| |_| | |  | || || |\  |
# |_|  |_/_/   \_\_| |_| \_\___/_/\_\ /_/   \_\____/|_|  |_|___|_| \_|
#                    Install script - Made by Stefan9110
                                                                    
# Sudo command; replace with doas if needed
AS_ROOT="sudo"
DESTINATION_DIR="/opt/matrix-admin-panel"
BIN_DIR="/bin"

FILES="
clioptions.py
color.py
main.py
commands.py
menu.py
install.sh
"

# If the script is run as root, do not require sudo
if [ $(whoami) = root ]; then
	AS_ROOT=""
fi

# Check whether a specific binary is installed on the sytem
function check_deps() {
	for dep in $@; do
		# Check if binary exists. If not, silently fail
		which $dep > /dev/null 2> /dev/null
		# Check exit code of the which command
		if [ ! $? -eq 0 ]; then
			echo "Binary dependency '$dep' is not installed..."
			exit 2
		fi
	done
}

function install() {
	# Check if already installed
	if [ -d $DESTINATION_DIR ]; then
		echo "Already installed. Please delete $DESTINATION_DIR if you want to reinstall."
		exit 1
	fi

	# Check binary dependencies 
	check_deps python pip

	echo "Installing pip requirements..."
	pip install -r requirements.txt

	echo "Creating $DESTINATION_DIR"
	$AS_ROOT mkdir -p $DESTINATION_DIR
	for i_file in $FILES; do
		echo "Copying $i_file to $DESTINATION_DIR/$i_file"
		$AS_ROOT cp $i_file $DESTINATION_DIR
	done

	echo "Linking $DESTINATION_DIR/main.py to $BIN_DIR/matrix-admin"
	$AS_ROOT ln -s $DESTINATION_DIR/main.py $BIN_DIR/matrix-admin
	echo "Installation successful :)"
}

function uninstall() {
	if [ ! -d $DESTINATION_DIR ]; then
		echo "Matrix admin is not installed on this system..."
		exit 1
	fi

	echo "Removing $DESTINATION_DIR and $BIN_DIR/matrix-admin"
	$AS_ROOT rm -r "$DESTINATION_DIR" "$BIN_DIR/matrix-admin"
	echo "Successfully uninstalled"
}

if [ ! $# -eq 0 ] && [ ! -z $1 ] && [ $1 = "-u" ]; then
	echo " --> Uninstalling matrix-admin <--"
	uninstall
else
	echo " --> Installing matrix-admin <--"
	install
fi
