# File Storage Architecture

## Evolution of Our File Storage System

---

# Phase 1 : Local Storage

Architecture:

Browser
    ↓
Flask API
    ↓
Local Disk (uploads folder)

Flow:

1. User uploads file.
2. Flask validates:
   - Extension
   - MIME Type
   - Size
   - Image Verification
3. File stored inside:

uploads/
├── profile/
└── attachments/

4. Metadata stored in DB.

---

## Advantages

- Very simple
- Fast for development
- Easy debugging
- No cloud cost

## Problems

- Files lost if server crashes
- Doesn't work with multiple servers
- Scaling issue
- Difficult backups
- Not suitable for production

---

# Phase 2 : Storage Abstraction Layer

Introduced:

StorageService (Interface)

Implementations:

1. LocalStorageService
2. S3StorageService

Factory Pattern:

get_storage()

Purpose:

Allow switching storage providers without changing business logic.

Architecture:

Service Layer
      ↓
Storage Factory
      ↓
Local / S3

---

# Phase 3 : AWS S3 Integration

Architecture:

Browser
     ↓
Flask
     ↓
Amazon S3

Bucket:

ankit-flask-notes-storage

Storage:

attachments/
profile/

Advantages:

- Durable (11 nines)
- Scalable
- Backups handled by AWS
- Multi-server support

---

# Phase 4 : Private Bucket

Bucket Access:

❌ Public Access Disabled

Files cannot be opened directly.

Reason:

Security.

Without this:

Anyone having URL can access files.

---

# Phase 5 : Presigned Download URLs

Architecture:

Browser
      ↓
Flask
      ↓
Generate Temporary URL
      ↓
Browser
      ↓
S3

Flow:

1. User requests download.
2. Flask verifies JWT.
3. Flask verifies ownership.
4. Generates temporary URL.
5. User downloads directly from S3.

Benefits:

- Bucket remains private.
- Backend bandwidth reduced.
- Secure temporary access.

Example:

GET /attachments/12/download

Response:

{
    "download_url": "...",
    "expires_in": 300
}

---

# Phase 6 : Presigned Upload URLs

Architecture:

Browser
      ↓
Flask (Generate URL)
      ↓
Browser
      ↓
S3

Purpose:

Avoid sending large files through backend.

Flow:

1. Request upload URL.
2. Upload directly to S3.
3. Notify backend.
4. Create DB row.

Benefits:

- Backend bandwidth almost zero.
- Supports very large files.
- Highly scalable.

---

# Current Upload Methods

## Method 1

Browser
    ↓
Flask
    ↓
S3

Used For:

- Small files
- Images
- PDFs

Pros:

- Simple
- Easy validation
- Checksum support

---

## Method 2

Browser
    ↓
S3

Used For:

- Large files
- Videos
- Production systems

Pros:

- Scalable
- Cheap
- Fast

Cons:

- More complex flow

---

# Current Database Structure

Attachment:

- filename
- original_filename
- mime_type
- file_size
- checksum
- note_id

Possible Future Improvements:

- storage_provider
- bucket_name
- s3_key
- etag
- upload_status

---

# Current Architecture Diagram

                    ┌──────────────┐
                    │   Browser    │
                    └──────┬───────┘
                           │
                    JWT Auth Request
                           │
                           ▼
                    ┌──────────────┐
                    │ Flask Backend│
                    └──────┬───────┘
                           │
               ┌───────────┴───────────┐
               │                       │
               ▼                       ▼
      Local Storage               Amazon S3
                                         │
                                         ▼
                            Presigned Upload/Download

---

# Future Improvements

1. Multipart Upload
2. CloudFront CDN
3. Lifecycle Rules
4. Virus Scanning
5. Thumbnail Generation
6. Background Processing
7. S3 Event Notifications
8. File Compression
9. Storage Analytics

---

# Interview Questions

### Why S3 instead of local storage?

- Scalability
- Durability
- Multi-server support

---

### Why Presigned URLs?

- Private bucket
- Temporary access
- Reduced backend load

---

### Why Direct Upload?

Backend should not process huge files.

Browser → S3 is cheaper and faster.

---

### How would you upload a 5GB file?

Use:

S3 Multipart Upload

---

### How to secure uploaded files?

- IAM Policies
- Private Bucket
- Presigned URLs
- JWT Ownership Verification

---

# Current Status

✅ Local Storage

✅ Storage Abstraction

✅ S3 Integration

✅ Presigned Downloads

✅ Presigned Uploads

✅ Upload Completion Flow

🔜 Multipart Uploads

🔜 CloudFront

🔜 Background Processing