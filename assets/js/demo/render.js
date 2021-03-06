!function(window, document, $, Pug) {
  var ListView = infinity.ListView,
      ListItem = infinity.ListItem,
      _ = require('underscore');

  var Posts = [];

  function getPost(i) {
    if (Posts.length >= i){
        return Posts[i];
    } else {
        Posts += loadPosts(Posts.length, i);
        return getPost(i);
    }
  }

  function loadPosts(start, end) {
    $.ajax({
      url: 'posts',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({posts: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error('comments.json', status, err.toString());
      }.bind(this)
    }); 
  }
      Pugs = Pug.images,
      PugNames = Pug.names,
      PugTaglines = Pug.taglines,
      PugStorage = Pug.storage;

  var pugTemplate = _.template($('#demo-pug-template').html()),
      doublePugTemplate = _.template($('#demo-double-pug-template').html());

  var column = $('#list-view'),
      pugCount = 0;

  var listView = new ListView(column, {
    lazy: function() {
      $(this).find('.pug').each(function() {
        var $ref = $(this);
        $ref.attr('src', $ref.attr('data-original'));
      });
    }
  });
  column.data('listView', listView);


  function pug() {
    var rotate, rotateRight, rotateLeft, name, caption, pugData;
    pugCount++;

    doublePug = Math.random() > 0.5;
    if (doublePug){
        tagline = _.template(PugTaglines[
          Math.floor(Math.random() * PugTaglines.length)
        ]);
        name1 = PugNames[Math.floor(Math.random() * PugNames.length)];
        name2 = PugNames[Math.floor(Math.random() * PugNames.length)];
        caption1 = tagline({name: name1});
        caption2 = tagline({name: name2});
        pugData1 = Pugs[Math.floor(Math.random() * Pugs.length)];
        pugData2 = Pugs[Math.floor(Math.random() * Pugs.length)];

        saved1 = PugStorage.check(pugData1.src, name, caption);
        saved2 = PugStorage.check(pugData2.src, name, caption);

        return doublePugTemplate({
          pug1: pugData1,
          pug2: pugData2,
          title1: name1,
          title2: name2,
          caption1: caption1,
          caption2: caption2,
          saved1: saved1,
          saved2: saved2,
        });
    } else {
        tagline = _.template(PugTaglines[
          Math.floor(Math.random() * PugTaglines.length)
        ]);
        name = PugNames[Math.floor(Math.random() * PugNames.length)];
        caption = tagline({name: name});
        pugData = Pugs[Math.floor(Math.random() * Pugs.length)];

        saved = PugStorage.check(pugData.src, name, caption);

        return pugTemplate({
          pug: pugData,
          title: name,
          caption: caption,
          saved: saved,
        });
    }
  }


  function row() {
      column.data('listView').append(pug());
  }

  function pb(num) {
    // Pugbomb! Fill in a smattering of num pugs
    var index;
    if(num <= 0) return;

    for(index = 0; index < num && index < 70; index++) {
      row();
    }
    num -= index;

    setTimeout(function() { pb(num - 1); }, 0);
  }

  Pug.bomb = pb;
  Pug.count = function() { return pugCount; };
}(window, document, jQuery, Pug);

