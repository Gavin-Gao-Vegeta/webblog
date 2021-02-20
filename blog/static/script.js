let li = document.getElementsByClassName('header-content')
for (let i = 0; i < li.length; i++) {
  li[i].addEventListener('mouseover', (e) => {
    e.target.parentNode.style.backgroundColor = 'black'
    e.target.style = 'color:white'
  })
  li[i].addEventListener('mouseout', (e) => {
    e.target.parentNode.style.backgroundColor = ''
    e.target.style = ''
  })
}
if (document.URL.match('login$|register$')) {
  let body = document.querySelector('body')
  body.style = 'overflow:hidden'
  let normal = document.getElementById('normal')
  let greeting = document.getElementById('greeting')
  let blindfold = document.getElementById('blindfold')
  let cont = document.getElementById('content-form');
  cont.removeAttribute('class')
  let close = document.querySelector('.close-btn')
  close.addEventListener('click', () => {
    window.history.back()
  })
  let normalStyle = document.getElementsByClassName('normal-style');
  let blindStyle = document.getElementsByClassName('blind-style');
  for (let i = 0; i < normalStyle.length; i++) {
    normalStyle[i].addEventListener('focus', () => {
      normal.style = 'display:none'
      greeting.style = ''
      blindfold.style = 'display:none'
    })
    normalStyle[i].addEventListener('blur', () => {
      normal.style = ''
      greeting.style = 'display:none'
      blindfold.style = 'display:none'
    })
  }
  for (let i = 0; i < blindStyle.length; i++) {
    blindStyle[i].addEventListener('focus', () => {
      normal.style = 'display:none'
      greeting.style = 'display:none'
      blindfold.style = ''
    })
    blindStyle[i].addEventListener('blur', () => {
      normal.style = ''
      greeting.style = 'display:none'
      blindfold.style = 'display:none'
    })
  }

}
let flashContent = document.getElementById('flashes')
if (flashContent.childElementCount > 0) {
  setTimeout(() => {
    let cnode = flashContent.childNodes;
    for (let i = cnode.length - 1; i >= 0; i--) {
      flashContent.removeChild(cnode[i])
    }
  }, 2000);
}
if (document.URL.match('post|login|register|about')) {
  let postContent = document.getElementById('content-form')
  postContent.removeAttribute('hidden')
}
let blogBtn = document.getElementsByClassName('blog-list')
for (let i = 0; i < blogBtn.length; i++) {
  // console.log(blogBtn[i].childNodes[1].childNodes[3].href)
  blogBtn[i].addEventListener('click', (e) => {
    window.location = blogBtn[i].childNodes[1].childNodes[3].href
  })
}

if (document.URL.match('search')) {
  let searchInput = document.getElementById('query')
  searchInput.value = document.URL.slice(document.URL.indexOf('=') + 1)
}