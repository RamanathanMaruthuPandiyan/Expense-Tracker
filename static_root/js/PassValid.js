function functionPasswordCheck() {
    var Password = document.getElementById('pass').value;
    var Re_Password = document.getElementById('re_pass').value;
    if (Password != Re_Password || document.getElementById('re_pass').value == '') {
        document.getElementById('Error').innerHTML = '*Password Did Not Match';
        document.getElementById('pass').value = '';
        document.getElementById('re_pass').value = '';
    } else {
        document.getElementById('Error').innerHTML = '';
    }
}
