# -*- coding: utf-8 -*-
import httplib, urllib, json
HOST_NAME = "web-ui.coolstore-dev-sourabh.svc"
PORT = 8080
test_count = 0
table_content = ""

def testResult(count,description,expected_value,actual_value):
    if(expected_value == actual_value):
        result = "Passed"
        class_result = "table-success"
    else:
        result = "Failed"
        class_result = "table-danger"
    content = "<tr class=\"%s\"><th scope=\"row\">%i</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(class_result,count,description,expected_value,actual_value,result)
    return content

# Test case 1 - Testing version URL
test_count = test_count+1
description = "/cart url should return 200 status code"
conn = httplib.HTTPConnection(HOST_NAME,PORT)
conn.request("GET","/#/cart")
response = conn.getresponse()
print response.status
result_content = testResult(test_count,description,200,response.status)
table_content = table_content + result_content
conn.close()

content = '<div class="container">\
    <table class="table">\
      <thead class="thead-dark">\
        <tr>\
          <th scope="col">#</th>\
          <th scope="col">Description</th>\
          <th scope="col">Expected</th>\
          <th scope="col">Actual</th>\
          <th scope="col">Result</th>\
        </tr>\
      </thead>\
      <tbody>\
        '+table_content+'\
      </tbody>\
    </table>\
  </div>\
  <nav class="navbar fixed-bottom navbar-expand-lg navbar-dark bg-dark ">\
    <a class="navbar-brand mx-auto" href="#">Copyright © 2018 Infosys Limited</a>\
  </nav>\
</body>\
</html>'

# f = open("./functional-test-result/header.html","r")
# header_content = f.read()
# f.close()

# f = open("./functional-test-result/index.html", "w+")
# f.write(header_content)
# f.write(content)
# f.close()
