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
.git/
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

	# Install pip requirements from requirements.txt
	echo "Installing pip requirements..."
	pip install -r requirements.txt

	# Copy required files to installation dir
	echo "Creating $DESTINATION_DIR"
	$AS_ROOT mkdir -p $DESTINATION_DIR
	for i_file in $FILES; do
		echo "Copying $i_file to $DESTINATION_DIR/$i_file"
		$AS_ROOT cp -r $i_file $DESTINATION_DIR
	done

	# Create binary simlink for main.py
	echo "Linking $DESTINATION_DIR/main.py to $BIN_DIR/matrix-admin"
	$AS_ROOT ln -s $DESTINATION_DIR/main.py $BIN_DIR/matrix-admin
	echo "Installation successful :)"
}

function uninstall() {
	# Check if matrix-admin is installed
	if [ ! -d $DESTINATION_DIR ]; then
		echo "Matrix admin is not installed on this system..."
		exit 1
	fi

	# Remove installation directory and binary symlink
	echo "Removing $DESTINATION_DIR and $BIN_DIR/matrix-admin"
	$AS_ROOT rm -r "$DESTINATION_DIR" "$BIN_DIR/matrix-admin"
	echo "Successfully uninstalled"
}

function update() {
	# Update local repo if it's not the same as the one in the installation directory
	if [ -d ".git/" ] && [ "$(pwd)" != "$DESTINATION_DIR" ]; then
		git pull
	fi

	# Update repo in the installation directory
	if [ -d $DESTINATION_DIR ]; then
		cd $DESTINATION_DIR
		$AS_ROOT git pull
	fi
}

# Print help message
function help_msg() {
	echo -e "Matrix Admin install script\n
options:
  -h  			show this help message and exit
  -r  			uninstall
  -u 	 		update
  no options	 	install"
}

# Option handling
if [ ! $# -eq 0 ]; then
	case $1 in
		"-r")
			echo " --> Uninstalling matrix-admin <--"
			uninstall
			;;
		"-u")
			echo " --> Updating matrix admin <--"
			update
			;;
		"-h")
			help_msg
			;;
		*)
			echo "Unknown option $1"
			;;
	esac
else
	echo " --> Installing matrix-admin <--"
	install
fi
