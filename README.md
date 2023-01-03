# EmailerTkinter
A simple Tkinter app to prepare E-Mails from predefined texts and contacts

This was made mainly to learn a multiframe/object oriented Tkinter approach while reducing time spend preparing E-Mails at work.
Runs with Sqlite3 and is customizable via the Config.txt (created at first run)

Mail_versender is the main file and the start of the program. Here the base frame object is defined and the others are loaded.

SelectorPageData is the first page visible when starting the app. Files can be droped into the Listbox via drag an drop or deleted by doubleclick. 
Contacts are grouped by text.
Both can be edited via doubleclick or via buttons

TODO: (cosmetic) add Labels to communicate DnD and doubleclick functions to user.



EditPageData is the page to edit contacts. 
New contacts are added via selecting the <new contact> option in the title spinner at the top.
When selecting <New text> in the text interface the user wil be redirected to the text edit page

TODO: (structural) find a way to rename file to ContactEditData.
TODO: (structural) find a way to group or sort titles in the spinner to prevent having to search when a lot of Contacts are present.


TextEditData is the page to edit the Text.
New text are added via selecting the <new text> option in the title spinner at the top.
The selections at the right can bee added to the text as placeholder and wil be replace at e-Mail creation as follows:
Contact Person - Name of the Contact,
File - The first file in the file list,
All files - all files in the file list,
Link - a Hyperlink to the directory where files will be moved (only when selected in the conctact edit)
Additional Info - any addional Info from the contact (this is a freeform entry to add flexibility)

TODO: (code) prevent "bug" where two linebreaks transform into two blank lines
