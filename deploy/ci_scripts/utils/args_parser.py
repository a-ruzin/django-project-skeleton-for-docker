def get_args(args_list: list[str]) -> dict[str, str]:
    return {
        item.split("=")[0].replace("--", ""): item.split("=")[1]
        for item in args_list
        if item.startswith("--")
    }
