import sass

# builds the perch.css file once. To watch the directory for changes, you can do:
# npm install -g watch
# watch scss:static/style

with open("perchweb/static/style/main.css", mode='w') as cssfile:
    cssfile.write(sass.compile(filename="perchweb/scss/perch.scss"))