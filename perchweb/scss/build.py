import sass

# builds the perch.css file once. To watch the directory for changes, you can do from the /perchweb directory:
# npm install -g sass
# sass --watch scss:static/style

with open("perchweb/static/style/perch.css", mode='w') as cssfile:
    cssfile.write(sass.compile(filename="perchweb/scss/perch.scss"))
