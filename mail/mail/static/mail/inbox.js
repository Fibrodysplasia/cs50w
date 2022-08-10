document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // When the send button is clicked, send the email
  document.querySelector('#compose-send').addEventListener('click', () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    send_email(recipients, subject, body);
  });
}

function reply_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';

      // Fill out composition fields
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = `RE: ${email.subject}`;
      document.querySelector('#compose-body').value = `
        On ${email.timestamp}, ${email.sender} wrote:
        ${email.body}
      `;

      // When the send button is clicked, send the email
      document.querySelector('#compose-send').addEventListener('click', () => {
        const recipients = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;
        send_email(recipients, subject, body);
    })
})}

function send_email(recipients, subject, body) {
  const request = new XMLHttpRequest();
  request.open('POST', '/emails');
  request.setRequestHeader('Content-Type', 'application/json');
  request.send(JSON.stringify({ recipients, subject, body }));
  load_mailbox('sent');
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the list of emails
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      emails.forEach(email => {
        document.querySelector('#emails-view').innerHTML += `
          <div style="display:flex; justify-content:space-between; border-style:dotted; padding:5px; margin-bottom:10px;">
            <div class="email">
              <div class="email-sender"><strong>From: </strong>${email.sender}</div>
              <div class="email-subject"><strong>Subject: </strong>${email.subject}</div>
              <div><strong>Time: </strong>${email.timestamp}</div>
            </div>
            <div>
              <button style="margin=right:0px;" class="email-button" id="${email.id}" onclick="load_email(${email.id})">View</button>
            </div>
          </div>
        `;
      });
    })
}


// Refactor this at some point
function load_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  const request = new XMLHttpRequest();
  request.open('GET', `/emails/${id}`);
  request.onload = () => {
    const email = JSON.parse(request.responseText);
    if (email.archived === false) {
      document.querySelector('#emails-view').innerHTML = `
        <div style="display:flex; justify-content:space-between; border-style:dotted; padding:5px;">
          <div class="email">
            <div class="email-sender"><strong>From: </strong>${email.sender}</div>
            <div><strong>Recipients: </strong>${email.recipients}</div>
            <div class="email-subject"><strong>Subject: </strong>${email.subject}</div>
            <div><strong>Time: </strong>${email.timestamp}</div>
          </div>
            <div>
              <button class="email-button" id="${email.id}" onclick="reply_email(${email.id})">Reply</button>
              <button class="email-button" onclick="archive_email(${email.id})">Archive</button>
            </div>
        </div>
        <div style="margin-top:0px; border-style: none dotted dotted dotted; padding:10px;" class="email-body">${email.body}</div>
      `;
    } else {
      document.querySelector('#emails-view').innerHTML = `
      <div style="display:flex; justify-content:space-between; border-style:dotted; padding:5px;">
        <div class="email">
          <div class="email-sender"><strong>From: </strong>${email.sender}</div>
          <div><strong>Recipients: </strong>${email.recipients}</div>
          <div class="email-subject"><strong>Subject: </strong>${email.subject}</div>
          <div><strong>Time: </strong>${email.timestamp}</div>
        </div>
          <div>
            <button class="email-button" id="${email.id}" onclick="load_email(${email.id})">View</button>
            <button class="email-button" onclick="unarchive_email(${email.id})">Un-Archive</button>
          </div>
      </div>
      <div style="margin-top:0px; border-style: none dotted dotted dotted; padding:10px;" class="email-body">${email.body}</div>
    `;
    }
}
  request.send();
}

function archive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ 
      archived: true
    })}
  )
  load_mailbox('inbox');
}

function unarchive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ 
      archived: false
    })}
  )
  load_mailbox('inbox');
  }
