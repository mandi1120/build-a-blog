import webapp2
import os
import jinja2
import cgi
from google.appengine.ext import db


#The /blog route displays the 5 most recent posts. 
#to limit the displayed posts in this way, you'll need to filter the query results.
#you have two templates, one for each of the main blog and new post views. 
#Your templates extend a base.html template which includes some boilerplate HTML 
#that will be used on each page, along with some styles to clean up your blog's 
#visuals a bit (you can copy/paste the styles from the AsciiChan exercise).
#You're able to submit a new post at the /newpost route/view. After submitting a 
#new post, your app displays the main blog page. Note that, as with the AsciiChan 
#example, you will likely need to refresh the main blog page to see your new post listed.
#If either title or body is left empty in the new post form, the form is rendered again, 
#with a helpful error message and any previously-entered content in the same form inputs.

#template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
#                               autoescape = True)
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
#class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    title = db.StringProperty(required = True)
    text = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
            
class MainPage(Handler):
    def render_front(self, title="", text="", error=""):
        blogs = db.GqlQuery("SELECT * from Blog "
                           "ORDER BY created DESC LIMIT 5;")
        self.render("front.html", title=title, text=text, error=error, blogs=blogs)


    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        text = self.request.get("text")

        if title and text:
#            self.redirect(###redirect here to blog listings page)
            a = Blog(title = title, text = text)
            a.put()
            self.redirect("/")
        else:
            error = "we need both a title and some text"
            self.render_front(title, text, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

