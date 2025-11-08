"""Entry point for running ico_to_svg as a module or executable."""

if __name__ == "__main__":
    from ico_to_svg.cli import main
    main()
else:
    from .cli import main
