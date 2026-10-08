MTSAD Thresholding Techniques

An undergraduate research project comparing thresholding techniques for multivariate time series anomaly detection (MTSAD).

Background

Anomaly detection models usually output a continuous anomaly score for each time step. A threshold then turns that score into a yes/no decision. A threshold that is too low causes false alarms, and one that is too high misses real anomalies. Choosing it well is one of the hardest parts of the pipeline, and no single method is known to work across all datasets.

Goal

This project compares existing thresholding methods on the same anomaly scores, so that the comparison is fair. It looks at how their performance changes across datasets, and it explores whether any method can be improved.

Research questions
RQ1: How do existing thresholding techniques perform, and how much does their ranking change across benchmark datasets?
RQ2: Does any single technique perform consistently well across datasets?
RQ3: Can existing techniques be improved, and in which direction (for example, combining EVT with channel-specific statistics, learned risk levels, or better drift handling)?









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

    
