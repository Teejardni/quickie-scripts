use colored::*;
use sysinfo::System;

fn main() {
    let mut sys = System::new_all();
    sys.refresh_all();

    let logo = vec![
    "IIIIIIIIII             GGGGGGGGGGGGG",
    "I::::::::I          GGG::::::::::::G",
    "I::::::::I        GG:::::::::::::::G",
    "II::::::II       G:::::GGGGGGGG::::G",
    "  I::::I        G:::::G       GGGGGG",
    "  I::::I       G:::::G              ",
    "  I::::I       G:::::G              ",
    "  I::::I       G:::::G    GGGGGGGGGG",
    "  I::::I       G:::::G    G::::::::G",
    "  I::::I       G:::::G    GGGGG::::G",
    "  I::::I       G:::::G        G::::G",
    "  I::::I        G:::::G       G::::G",
    "II::::::II       G:::::GGGGGGGG::::G",
    "I::::::::I        GG:::::::::::::::G",
    "I::::::::I          GGG::::::GGG:::G",
    "IIIIIIIIII             GGGGGG   GGGG",
];
    let info = vec![
        format!("{}", std::env::var("USER").unwrap_or_else(|_| "unknown".to_string()).bright_cyan()),
        format!("{}: {}", "OS".bright_green(), System::name().unwrap_or_else(|| "Unknown".to_string())),
        format!("{}: {}", "Kernel".bright_green(), System::kernel_version().unwrap_or_else(|| "Unknown".to_string())),
        format!("{}: {}", "Uptime".bright_green(), format_uptime(System::uptime())),
        format!("{}: {}", "Shell".bright_green(), std::env::var("SHELL").unwrap_or_default().split('/').last().unwrap_or("unknown")),
        format!("{}: {} MB / {} MB", "Memory".bright_green(), 
            sys.used_memory() / 1024 / 1024, 
            sys.total_memory() / 1024 / 1024),
    ];

    for (i, line) in logo.iter().enumerate() {
        print!("{}  ", line.bright_blue());
        if i < info.len() {
            println!("{}", info[i]);
        } else {
            println!();
        }
    }
}

fn format_uptime(seconds: u64) -> String {
    let hours = seconds / 3600;
    let minutes = (seconds % 3600) / 60;
    format!("{}h {}m", hours, minutes)
}
