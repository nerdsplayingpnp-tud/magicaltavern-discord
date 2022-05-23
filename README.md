<div id="top"></div>




<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/bitfl0wer/magicaltavern">
    <img src="https://cdn.discordapp.com/avatars/959837234033475584/744a62cb7f9f8e94931e1400a6ea45f4.png?size=256" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">magicaltavern</h3>

  <p align="center">
    Organize your PnP Sessions.
    <br />
    <br />
    <a href="https://github.com/bitfl0wer/magicaltavern/issues">Report Bug</a>
    ·
    <a href="https://github.com/bitfl0wer/magicaltavern/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Welcome to the magical tavern! Travelers and adventurers from far and wide gather here to discuss their next adventure or simply just meet over a good ol' pint of beer.

### Okay so... what is this *really*?
magicaltavern is a Discord Bot written in python that aims to organise D&D/PnP Discord Servers by providing handy tools.
These tools include:
<br />
- Commands to find players for a PnP campaign
- A database integration to store interested members and automatically create a server cateory and roles for them to 
talk in
- Cool things

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [py-cord](https://docs.pycord.dev/en/master/)
* [sqlite3](https://www.sqlite.org/index.html)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Here are some instructions to self-host the bot. The bot currently has no public instances and does not support public
instances either.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* [python 3.9](https://www.python.org/downloads/)
* pip
  ```sh
  python -m ensurepip --upgrade
  ```
  

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/bitfl0wer/magicaltavern.git
   ```
2. (Optional) Create and activate a venv in the project directory
    <br/>
Linux and macOS:
    ```sh
   python -m venv venv
   source ./venv/bin/activate
   ```
3. Install pip requirements
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your bot token in `config/token.txt`
   ```
   OTD4ODM4XhA0rDMzNDfXX44NTg1/kasjDFG_93ajksdhjk.ahjk1olnmqFAafdzfdsyui
   ```
5. Modify the files in the `/config` directory to fit your needs. In `config/config.json`, set the `guilds` attribute to
the id(s) of the guilds you want the bot to operate in. Also, do not forget to create a role for dungeon masters on your
server. Copy the ID of that role into `config/roles.json` as the `role-dm` attribute. Do the same thing for the admin
role, and finally, put the user ID of the person that is supposed to be the bots' owner under `id-owner`.
6. Start the bot. From the project source (magicaltavern/) type
    ```sh
    python -m src.bot
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Not done yet. WIP!
<br/>
_For more examples, please refer to the [Documentation](https://www.youtube.com/watch?v=dQw4w9WgXcQ)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/bitfl0wer/magicaltavern/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the AGPL-3.0 License.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Flori - [@starflowerflori](https://twitter.com/starflowerflori) - florian@proweber.de

Project Link: [https://github.com/bitfl0wer/magicaltavern](https://github.com/bitfl0wer/magicaltavern)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Yama](https://github.com/OParczyk) for helping me figure out sqlite stuff! <3


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bitfl0wer/magicaltavern.svg?style=for-the-badge
[contributors-url]: https://github.com/bitfl0wer/magicaltavern/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bitfl0wer/magicaltavern.svg?style=for-the-badge
[forks-url]: https://github.com/bitfl0wer/magicaltavern/network/members
[stars-shield]: https://img.shields.io/github/stars/bitfl0wer/magicaltavern.svg?style=for-the-badge
[stars-url]: https://github.com/bitfl0wer/magicaltavern/stargazers
[issues-shield]: https://img.shields.io/github/issues/bitfl0wer/magicaltavern.svg?style=for-the-badge
[issues-url]: https://github.com/bitfl0wer/magicaltavern/issues
[license-shield]: https://img.shields.io/github/license/bitfl0wer/magicaltavern.svg?style=for-the-badge
[license-url]: https://github.com/bitfl0wer/magicaltavern/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
