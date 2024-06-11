var formdata = new FormData();
formdata.append("video", fileInput.files[0], "D:\code\VD\Violence-Alert-System\Completed Project\V_19.mp4");

var requestOptions = {
  method: 'POST',
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/detect_violence", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));