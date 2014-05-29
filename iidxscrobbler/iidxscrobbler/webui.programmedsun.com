
<!DOCTYPE html>
<html>
    <head>
        <link rel="icon" type="image/vnd.microsoft.icon" href="http://webui.programmedsun.com/static/favicon.ico">
        <style type="text/css">            
            a {
                font-weight: bold;
                color: #888;
            }
            
            a:visited {
                color: #888;
            }

            body {
                font-family: sans-serif; 
                font-size: 10pt; 
                color: #888;
            }

            hr {
                height: 1px;
                border: none;
                background-color: #888;
                margin: 0.2em 0;
            }
            
            input {
                border: 1px solid #888;
                background-color: #eee;
                color: #444;
            }
            
            label {
                float: left;
                width: 10em;
                font-weight: bold;
            }

            .err {
                color: #800;
            }
            
            .field {
                width: 15em;
            }
            
            .formrow {
                margin: 0.2em;
            }
            
            #center {
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                margin: auto;
                width: 40em;
                height: 9em;
            }
            
            #inner {
                width: 30em;
                margin-top: 1em;
                margin-bottom: 1em;
                margin-left: auto;
                margin-right: auto;
            }
            
            #submit {
                float: right;
                width: 5em;
            }
        </style>
        <title>you are now entering completely darkness</title>
    </head>
    <body>
        <form method="POST">
            <div id="center">
                <div id="links">
                              <a class="" href="/activate">activate account</a>

                    |         <a class="" href="/pwreset">forgot password</a>

                    | <a href="mailto:darknao@bemaniso.ws">contact us</a>
                </div>
                <hr>
                <div id="inner">
                    <div class="formrow">
                        <label for="username">username:</label>
                        <input name="username" class="field" value="" >
                    </div> 
                    <div class="formrow">
                        <label for="password">password:</label>
                        <input name="password" class="field" value="" type="password">
                    </div>
                </div>
                <hr>
                <span class="err">
                </span>
                <input id="submit" type="submit" value="log in">
            </div>
        </form>
    </body>
</html>
