---
## 💭 First Step:
run these two commands
```bash 
pip install -r requirements.txt
``` 
```bash 
pre-commit install -f
```

## 🛠️ Troubleshooting

### Windows: "cannot spawn .git/hooks/pre-commit: No such file or directory"
This happens on Windows when the hook file is incompatible. Fix it by running:

```bash
Remove-Item ".git\hooks\*" -Force
pre-commit install -f
```

### Windows: "OSError: [WinError 193] %1 is not a valid Win32 application"
This happens when an old broken hook is conflicting. Fix it by running:

```bash
Remove-Item ".git\hooks\*" -Force
pre-commit install -f
```

Then try your commit again:
```bash
git commit -m "your message"
```
## Important Notes for Beginners

Your three best friends among Git commands are:

```bash
git add .
```

```bash
git commit -m "your message"
```

```bash
git push
```

## ⚠️ Things to Remember

1. Always make sure you are on the correct branch before committing
2. After running `git commit -m` pre-commit checks will run automatically; these act as filters to keep your code clean and consistent
3. If pre-commit makes any changes to your files run `git add .` again before committing; otherwise those fixes won't be included
4. Never push directly to main; always work on a branch and open a Pull Request

    
