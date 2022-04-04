
async function requestData() {
    const response = await fetch("/root/peoples/", {method: 'GET'});
    const data = await response.json();
    const str = JSON.stringify(data, undefined, 4)
    document.getElementById("responseBox").innerHTML = ''
    document.getElementById("responseBox").appendChild(document.createElement('pre')).innerHTML = str;
    console.log(data);
}

async function addPerson() {
    const name = document.getElementById("name").value
    const surname = document.getElementById("surname").value
    await postData("/root/peoples/", {"name": name, "surname": surname});
    await requestData();
}

async function clearTable() {
    console.log("clearing")
    const id = document.getElementById("removeId").value
    await remove("/root/peoples/" + id);
    await requestData();
}

async function remove(url = '') {
    return await fetch(url, {
          method: 'DELETE',
          headers: {
              'X-CSRFToken': 'BhOmkEsNGMdPEGfjaHGQ46gy626OFJx5tBkNatwR11c4OxLnvlQzPqdScO4g8NmA',
              'Content-Type': 'application/json'
          },
      });
}

async function postData(url = '', data = {}) {
      const response = await fetch(url, {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            headers: {
                  'X-CSRFToken': 'BhOmkEsNGMdPEGfjaHGQ46gy626OFJx5tBkNatwR11c4OxLnvlQzPqdScO4g8NmA',
                  'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
      return response.json(); // parses JSON response into native JavaScript objects
}