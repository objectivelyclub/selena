const express = require('express')  
const fs = require('fs');
const app = express()  
const port = 3000

app.get('/', (request, response) => {  
  response.send('Hello from Express!')
})

var walkSync = function(dir, filelist) {
  var fs = fs || require('fs'),
      files = fs.readdirSync(dir);
  filelist = filelist || [];
  files.forEach(function(file) {
    if (fs.statSync(dir + '/' + file).isDirectory()) {
      filelist = walkSync(dir + file + '/', filelist);
    }
    else {
      filelist.push(file);
    }
  });
  return filelist;
};

app.get('/load/images', (req, res) => {
  fn = walkSync(__dirname + "/images")
  res.send(JSON.stringify(fn));
})

app.use(express.static(__dirname + '/public'));

app.listen(port, (err) => {  
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log(`server is listening on ${port}`)
})
