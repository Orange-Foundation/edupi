I. Connection & Login to CMS
============================

1. Go to the url 'http://edupi.fondationorange.org:8021/custom/' and jump into a login page.
(the port number is configured in nginx)

2. When authenticated with admin username and password, jump into the CMS home page.


II. Configuration of Directories
================================

1. Create root directories.

    In the home page, click `Create Directory` to create a `root directory`.
    We can see the result instantly.

2. Create sub directories.

    Click a root directory to enter into it, then click `Create Directory` to create a sub-directory
    under the current directory.

3. Change a directory's name.

    Click `Edit` on a directory row to enter a new name.

4. Delete a directory.

    Click `Delete` on a directory row to delete a directory.
    this action will also delete recursively all its sub directories.
    However, its documents will not be deleted.
    Danger: there is no `undo` for this action.

5. Move a sub-directory to root.

    Click `Unlink` on a directory row to move a sub-directory to the root.

6. Move a root directory to current directory.

    Suppose we are in a directory, we click the button `link a directory` to link a root directory to the current
    directory. The root directory then becomes a sub-directory of the current directory.

7. Navigation between the documents

    When entered into a directory, click the names on the navigation bar to go back to previous directories.


III. Upload & Configure Documents
=================================

1. Upload documents.

    When inside a directory, click `Upload` button to enter into the upload page.
    Then use drag-and-drop to upload documents.

    When uploading, the `finish` button is blocked.
    When upload finished, click the `finish` button go back to the directory.

2. Modify documents' META data.

    Click `Edit glyphicon` on a document to modify its `name`, `description`, etc.

3. Link a document.

    Click `Link documents` button under a directory to add existed documents from the server.

4. Unlink a document.

    Click `Unlink glyphicon` to unlink a document from the current directory.
    The unlinked document is not deleted from the server and may be linked by other directories.

5. Delete a document.

    Click `Delete glyphicon` to delete a document from the server.
    When a document is deleted, it's deleted from all the referenced directories.
    Danger: there is no `undo` for this action.

6. View a document online.

    Click the document's name to view the document with the browser.

7. Download a document.

    Click the `Download glyphicon` to download a document from the server.
