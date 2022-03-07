# Matrix Admin Panel
This is a tool that aims to provide easy [admin api](https://matrix-org.github.io/synapse/latest/usage/administration/admin_api/) access to [Matrix Synapse](https://matrix.org/) homeserver admins. This is a terminal user interface written in Python 10.

## Table of contents
* [FAQ](#faq)
* [Features](#features)
* [Instsallation](#instasllation)
* [Usage]()
* [License](#license)
* [Contributing](#contributing)

## FAQ
**Q**: *Why python for such a simple tool?*\
**A**: This was first intended to be written in *bash*, however matrix synapse api provides json responses which are easier to handle in python, and python provides compatibility with non unix platforms.

**Q**: *What happens with my authentication token?*\
**A**: I know that entering your matrix  account's authentication token in a random script online is not the best security practice, however the token is never stored on disk nor uploaded anywhere, and is read silently from stdin (check [main.py]())

**Q**: *I did a mistake and accidentally deleted/deactivated a room/user account...*\
**A**: Such actions are permanent actions and cannot be reverted. Please **double check**  before executing any action with this tool. I am not responsible for what goes wrong with it. Also **note that this tool is still heavily untested**, so bugs may occur which can negatively affect your homeserver. If you found any bug, please create an issue and I will try to get it fixed asap.

**Q**: *Is there a CLI alternative to this tool?*\
**A**: I am planning on creating a CLI version in the near future.

## Features
#### Users
* List registered users on the homeserver
* Search for a registered user
* Deactivate an user account

#### Registration tokens
* Create registration token
* List active registration tokens
* Delete a registration token

#### Rooms
* List all rooms created on the homeserver
* Search for a room on the homeserver
* Delete/Purge/Block a room

## Installation

## Usage

## License
This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for more details.

## Contributing
Contributing is highly appreciated. Any bug fixes or implementation improvements can go straight into a pull request. If you want to implement an extra feature, please create a **feature request** issue first.
