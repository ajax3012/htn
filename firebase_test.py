from firebase import firebase

firebase = firebase.FirebaseApplication('https://nguoilaoi-88576-default-rtdb.firebaseio.com/', None)
data =  { 'Name': 'John Doe',
          'RollNo': 3,
          'Percentage': 70.02
          }         
result = firebase.post('/nguoilaoi',data)
