WORKDIR = StripeTestTask

style:
    black -S -l 79 $(WORKDIR)
    isort $(WORKDIR)
    mypy $(WORKDIR)
    flake8 $(WORKDIR)
    djhtml -i -t 2 StripeTestTask/templates
