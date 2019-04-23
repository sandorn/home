  <html>
    <head>
      <title>A Demo Page</title>

      <script language="javascript">
        // Completes the full-name control and
        // shows the submit button
        function completeAndReturnName() {
          var fname = document.getElementById('fname').value;
          var lname = document.getElementById('lname').value;
          var full = fname + '' + lname;

          document.getElementById('fullname').value = full;
          document.getElementById('submit-btn').style.display = 'block';

          return full;
        }
      </script>
    </head>

    <body>
      <form>
        <label for="fname">First name:</label>
        <input type="text" name="fname" id="fname"></input>
        <br />
        <label for="lname">Last name:</label>
        <input type="text" name="lname" id="lname"></input>
        <br />
        <label for="fullname">Full name:</label>
        <input disabled type="text" name="fullname" id="fullname"></input>
        <br />
        <input style="display: none;" type="submit" id="submit-btn"></input>
      </form>
    </body>
  </html>