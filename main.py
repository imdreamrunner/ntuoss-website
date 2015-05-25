#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from common import JINJA

APP_ID = "__REMOVED__"
APP_SECRET = "__REMOVED__"

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        t = JINJA.get_template('home.html')
        self.response.write(t.render())


class JoinMailingListHandler(webapp2.RequestHandler):
    def post(self):
        email = self.request.get("email")
        import gdata
        self.response.headers['Content-Type'] = 'application/json'
        import json
        ret = {
            "status": 0,
            "email": email
        }
        self.response.write(json.dumps(ret))


class HacksPageHandler(webapp2.RequestHandler):
    def get(self):
        t = JINJA.get_template('hacks.html')
        self.response.write(t.render())


class HacksEventsHandler(webapp2.RedirectHandler):
    def get(self):
        import facebook
        access_token = facebook.get_app_access_token(APP_ID, APP_SECRET)
        graph = facebook.GraphAPI(access_token)
        result = graph.request("/ntuoss/events", {
            "since": 0,
            "fields": ["name", "cover", "picture", "start_time", "location"]
        })
        events = result['data']
        return_event_list = []
        for event in events:
            if "cover" in event:
                cover = event['cover']['source']
            else:
                cover = None
            return_event_list.append({
                "id": event['id'],
                "name": event['name'],
                "cover": cover,
                "picture": event['picture']['data']['url'],
                "location": event['location'],
                "start_time": event['start_time']
            })
        import json
        return_object = {
            "status": 0,
            "data": return_event_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(return_object))


class ProjectsPageHandler(webapp2.RequestHandler):
    def get(self):
        t = JINJA.get_template('projects.html')
        self.response.write(t.render())


class LessonsPageHandler(webapp2.RequestHandler):
    def get(self):
        t = JINJA.get_template('lessons.html')
        self.response.write(t.render())


class SponsorshipPageHandler(webapp2.RequestHandler):
    def get(self):
        t = JINJA.get_template('sponsorship.html')
        self.response.write(t.render())


class BlogPageHandler(webapp2.RequestHandler):
    def get(self):
        t = JINJA.get_template('blog.html')
        self.response.write(t.render())


app = webapp2.WSGIApplication([
    ('/', HomePageHandler),
    ('/join-mailing-list', JoinMailingListHandler),
    ('/tgifhacks/', HacksPageHandler),
    ('/tgifhacks/events', HacksEventsHandler),
    ('/projects/', ProjectsPageHandler),
    ('/lessons/', LessonsPageHandler),
    ('/sponsorship/', SponsorshipPageHandler),
    ('/blog/', BlogPageHandler)
], debug=True)
