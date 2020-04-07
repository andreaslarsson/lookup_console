# Lookup console
Easy to use console application to lookup synonyms and definitions. 

### Setup
```
git clone https://github.com/andreaslarsson/lookup_console.git
cd lookup_console
pip3 install -r requirements.txt
```

### Add function to shell
```
function <ALIAS>() {
    lookup_path='<PATH_TO_LOOKUP_CONSOLE>/lookup_console.py'
    python3 $lookup_path $1 $2
}
```

### Usage
```
# Get synonyms for 'test'
<ALIAS> test

# Get definitions for 'test'
<ALIAS> test -d
```

