import bcrypt

def hash_password(password: str) -> str:
    # Convert password string to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a secure salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Convert back to a clean string to store safely in PostgreSQL
    return hashed_password_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check if the incoming plain password matches the hashed string from the DB
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )