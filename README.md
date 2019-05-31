**THIS IS A FORKED, IN-DEVELOPMENT VERSION OF COG**

If you're looking for a working copy of the original cog, please visit https://github.com/techx/cog.

---

# Cog

Cog is a hardware checkout system for hackathons, originally written for use
at HackMIT and MakeMIT, now forked by Hack the North.

![Cog](/media/cog.png?raw=true)

## Features

### Inventory Management
Add inventory items individually or in bulk from a spreadsheet, providing
links and descriptions to give hackers resources for getting started. Items
can even be individually named and tracked to make sure nothing goes missing.

### Flexible Request System
Tweak Cog to fit the logistical needs of your event, with options to manage
lotteried items, items that require checkout, or simply a grab-and-go style
inventory.

### Keep Track of Users
Easily determine which hackers have which items, and get in touch with
hackers via phone or email. You can additionally track whether or not you've
collected collateral (such as an ID) from each hacker.

### Real-time Admin Panel
View, approve, and fulfill item requests in real-time as they come in. As
soon as an organizer approves a request, hackers can see that their item is
ready to be picked up.

## Deployment & Configuration

Cog is written in Python 3 (at least our fork partially is) and uses PostgreSQL as a
database. Hack the North's fork of Cog is configured with `docker-compose` for local development and deploys to Kubernetes through Skaffold.

A myriad of configuration options are available to be tweaked in
[`config.py`](cog/config.py). Alternatively, all values set in
this file can be set as environment variables of the same name - environment
variable values will take precedence over the value specified in `config.py`.
Sensible defaults are in place for all of the event logistical settings, but
we recommend playing around with them a bit. At the bare minimum you
should change the `HACKATHON_NAME` and set your `SECRET` env
variables.


### Adding Hardware via Google Sheets
While you can add individual items one-by-one, we recommend creating a
spreadsheet with all your items and importing this into Cog in one go.
Currently, the only supported way to do this is via Google Sheets. An example
Cog inventory sheet can be found
[here](https://docs.google.com/spreadsheets/d/1ZCHa_F3i0vyoZtjJNyNhBg-flRBs-DUIT1GtKC26P14/edit#gid=0).

To import from a Google Sheet, simply turn on view-only sharing and paste the
main URL (not the sharing URL) into Cog after clicking 'Import Google Sheet'
on the main inventory page.

### Customizing Branding
Cog uses the [Semantic UI](https://semantic-ui.com/) framework for styling.
Branding can easily be customized using Semantic UI
[themes](https://semantic-ui.com/usage/theming.html).

While Cog mostly uses default Semantic UI styling, a minimal amount of custom
CSS lives in `cog/static/sass/app.scss`. In order to rebuild the
CSS when the Sass is changed, install [Sass](https://sass-lang.com/) and run
`sass --watch sass:css` in the `/static` directory.

*If you end up using Cog for your event, please take a moment to add yourself to our 
[users list](https://github.com/techx/cog/wiki/Cog-Users)!*

## Development
**Here be dragons**

Interested in hacking on Cog? Check out the [development guide](DEVELOPMENT.md) 
for some steps to get you started.

## Contributing
Hacking on Cog go well? Contribute back to upstream! We love outside
contributions - have a look at our [contributing guide](CONTRIBUTING.md) for
information on how you can get involved.

## Acknowledgements

**Pre-fork acknowledgements**  

Thanks to the following folks for their contributions to Cog pre-open
sourcing: 
- [Ethan Weber](https://github.com/ethanweber) and [Albert
Yue](https://github.com/albert-yue) of [MakeMIT](https://makemit.org) 
- [Shreyas Kapur](https://github.com/revalo) of [HackMIT](https://hackmit.org)
- [Andrew Zhang](https://github.com/zhangcandrew) of [SwampHacks](http://swamphacks.com)

## License
Copyright 2017-2018 [Noah Moroze](mailto:me@noahmoroze.com). Released under
AGPLv3. See [LICENSE.md](LICENSE.md) for a copy of the full license text. 