# Bytememo (Noteapp)
A note-taking app for casual users featuring a flexible method for organizing notes which can help users to find notes faster and remember notes better. 

Notes are grouped using tags, which allows for each note to be organized under multiple tags as the user sees fit. This removes the restriction of using folders where each note can only be organized under a single folder. 

#### Background
I started with a [YouTube tutorial](https://youtu.be/dam0GPOAvVI) and evolved the project into something unique, addressing some of my issues with Evernote as a longtime user. Along the way, I have picked up skills in full-stack web dev.

The main issue was how to sort a note which ostensibly belongs in more than one notebook. For example, I had trouble deciding whether to put a note I took from a YouTube video on running in my 'Fitness' or 'Learning' notebook. These hiccups are minor but can be frustrating over time. 

I was inspired by Cyberspace in Cyberpunk 2077 and the Data Cloud in Citizen Sleeper, with the idea of streams of consciousness flowing in an interconnected web. It was along these lines that I thought of doing away with folders, and connecting notes using tags alone. The current product is a working prototype of the idea. 

## Preview

![landing page](https://i.imgur.com/Cn9PIVh.png)This is what it looks like when someone first enters the site. I used Figma to design the bento layout before building it in HTML and CSS. 

![signup page](/website/static/img/signup.gif)

Embracing the cyberpunk theme, I created a signup page which was inspired by glowing neon signs (the GIF is sped up). 

<img src="https://i.imgur.com/w71KQoC.png" width="320">

After signing in, users can create and edit tags in the edit page. The up and down arrows allow for reordering of tags. 

<img src="https://i.imgur.com/e10Y812.png" width="240">

After updating the tags, the sidebar shows the current tags. Users can filter tags by clicking on individual tags.

![editing a note](https://i.imgur.com/CJARswP.png)This is how editing a note looks like with the integrated Quill.js, a minimal toolbar with relevant formatting tools. 

![dashboard](https://i.imgur.com/i1eMy0N.png)A populated dashboard. Notes are ordered by when they were last saved. 

The app is currently deployed at https://bytememo.onrender.com on a live PostgreSQL database.

## Learning points

### Backend development

#### Flask framework
- Designed a scalable Flask application using the application factory pattern
- Organized routes using Flask blueprints
- Created custom error handlers for 400, 404 and 500 errors

#### Database 
- Designed hierarchical relationships (parent-child for tags), building a double-layered tagging system 
- Created complex database relationships including many-to-many between notes and tags
- Implemented foreign key constraints to maintain data integrity, preventing invalid references in relational tables

### Frontend development

#### HTML templating
- Designed a modular HTML template system with Jinja2
- Implemented conditional rendering of the sidebar based on user state
- Created blocks (header, footer, navigation) for consistent layouts 

#### User interface (UI)
- Developed a tag management system with Javascript DOM manipulation, allowing users to create, edit, and organize tags dynamically
- Implemented tag autocompletion with AJAX
- Integrated rich text editing using Quill.js 

### Full-stack integration
- Developed RESTful API endpoints for frontend-backend communication
- Managed form submissions and validation of user inputs

### Security
#### User authentication
- Implemented login/signup flows using Flask-Login
- Applied hashing using bcrypt for secure password storage
- Utilized `@login_required` decorator to protect private routes

#### Form security
- Sanitized user input with Bleach to protect against XSS attacks
- Added CSRF protection using WTForms to protect against cross-site forgery

#### Web security
- Enforced HTTPS and content security policies with Flask-Talisman 

### Development best practices
#### Project layout
-  Organized folder and file structure adhering to Flask conventions
- Separated application logic into logical directories (e.g., `app`, `models`, `routes`, `templates`, `static`)

#### Development tools
- Utilized `pipenv` virtual environment for isolated dependency management
- Implemented package management using `pip` and `requirements.txt`
- Implemented version control using Git

## Future Work
- [ ] Learn how to use testing Frameworks and tools to make it easier to catch bugs and debug
- [ ] Responsive design for mobile devices
- [ ] Autosave feature

## Image Credits
Rob Shields 
- https://www.deviantart.com/robshields/art/Glitter-Girl-Face-Off-7-696416063
- https://www.deviantart.com/robshields/art/Angel-Face-Off-3-689613485
- https://www.deviantart.com/robshields/art/Trace-Face-684881673
- https://www.deviantart.com/robshields/art/Dr-Know-Face-Off-4-690634462
- https://www.deviantart.com/robshields/art/Special-Delivery-Animated-647357650

Koyorin 
- https://www.deviantart.com/koyorin/art/lucky-you-904507644
