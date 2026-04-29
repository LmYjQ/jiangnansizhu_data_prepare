use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread;
use std::time::Duration;

use midir::{MidiInput, MidiInputConnection};
use serde::{Deserialize, Serialize};
use tauri::{AppHandle, Emitter};

// MIDI 音符事件
#[derive(Clone, Serialize, Deserialize)]
pub struct MidiNoteEvent {
    pub note: u32,
    pub velocity: u32,
}

// 存储运行状态
static MIDI_RUNNING: AtomicBool = AtomicBool::new(false);

#[tauri::command]
fn start_midi_listener(app: AppHandle) -> Result<String, String> {
    log::info!("启动 MIDI 监听器...");

    // 如果已经在运行，直接返回
    if MIDI_RUNNING.load(Ordering::SeqCst) {
        return Ok("MIDI已经在运行".to_string());
    }

    let running = Arc::new(AtomicBool::new(true));
    let running_clone = running.clone();
    let app_clone = app.clone();

    // 在后台线程启动 MIDI 监听
    thread::spawn(move || {
        // 初始化 MIDI 输入
        let mut midi_in = match MidiInput::new("Jianpu Editor MIDI Input") {
            Ok(m) => m,
            Err(e) => {
                log::error!("创建MIDI输入失败: {}", e);
                let _ = app_clone.emit("midi-error", format!("创建MIDI输入失败: {}", e));
                return;
            }
        };

        // 获取可用的 MIDI 端口
        let ports = midi_in.ports();
        if ports.is_empty() {
            log::warn!("未发现MIDI设备");
            let _ = app_clone.emit("midi-error", "未发现MIDI设备");
            return;
        }

        log::info!("发现 {} 个 MIDI 端口", ports.len());

        // 保持连接
        let mut connection: Option<MidiInputConnection<()>> = None;

        // 尝试连接每个端口
        for port in &ports {
            let midi_in_port = match MidiInput::new("Jianpu Editor MIDI Input") {
                Ok(m) => m,
                Err(_) => continue,
            };

            let port_name = midi_in_port.port_name(port).unwrap_or_else(|_| "未知设备".to_string());
            log::info!("尝试连接: {}", port_name);

            let app_emitter = app_clone.clone();

            match midi_in_port.connect(
                port,
                "JianpuEditor",
                move |_stamp: u64, message: &[u8], _data: &mut ()| {
                    // 解析 MIDI 消息
                    if message.len() >= 3 {
                        let status = message[0];
                        let note = message[1] as u32;
                        let velocity = message[2] as u32;

                        // 只处理 Note On 消息且力度 > 0
                        if (status & 0xF0) == 0x90 && velocity > 0 {
                            log::debug!("MIDI Note: {} Velocity: {}", note, velocity);
                            let event = MidiNoteEvent { note, velocity };
                            let _ = app_emitter.emit("midi-note", event);
                        }
                    }
                },
                (),
            ) {
                Ok(conn) => {
                    log::info!("已连接到: {}", port_name);
                    let _ = app_clone.emit("midi-connected", port_name);
                    connection = Some(conn);
                    break;
                }
                Err(e) => {
                    log::warn!("连接 {} 失败: {}", port_name, e);
                }
            }
        }

        if connection.is_none() {
            let _ = app_clone.emit("midi-error", "无法连接到任何MIDI设备");
            return;
        }

        // 标记为运行中
        MIDI_RUNNING.store(true, Ordering::SeqCst);

        log::info!("MIDI 监听中...");

        // 保持监听直到被停止
        while running_clone.load(Ordering::SeqCst) {
            thread::sleep(Duration::from_millis(10));
        }

        // 断开连接
        drop(connection);
        MIDI_RUNNING.store(false, Ordering::SeqCst);
        log::info!("MIDI 监听已停止");
    });

    Ok("MIDI监听器已启动".to_string())
}

#[tauri::command]
fn stop_midi_listener() -> String {
    log::info!("停止 MIDI 监听器...");
    MIDI_RUNNING.store(false, Ordering::SeqCst);
    "MIDI监听器已停止".to_string()
}

#[tauri::command]
fn get_midi_status() -> bool {
    MIDI_RUNNING.load(Ordering::SeqCst)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // 初始化日志
    let _ = env_logger::Builder::from_env(
        env_logger::Env::default().default_filter_or("info")
    ).try_init();

    log::info!("启动简谱编辑器...");

    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            start_midi_listener,
            stop_midi_listener,
            get_midi_status
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}