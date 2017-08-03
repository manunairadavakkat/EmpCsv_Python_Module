/**
 * Created by manuadavakkat on 29/07/2017.
 */

    function FormValidate() {
               var input = document.getElementById("uploadfile").value;
               if (input.length == 0)
               {
                   alert("Please select a file to Upload")

               }
              var inputname = document.getElementById("uploadfile").name;

             if (input.length != 0)
             {
                 var ext = (input.substr(input.lastIndexOf('.') + 1)).toLowerCase();
                 if (ext == 'csv')
                 {
                     $("#msg").text("Files are supported")

                 }
                 else {
                     alert("Files are NOT supported. Please Upload csv file only")
                     return;

                 }
             }

}
