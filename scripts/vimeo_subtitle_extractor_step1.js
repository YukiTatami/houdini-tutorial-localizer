// Vimeo字幕取得スクリプト - ステップ1: Player初期化・字幕収集
// 使用方法: Vimeo埋め込みページの開発者ツールConsoleで実行

let transcriptData = [];
let processingStats = { totalCues: 0, duplicatesSkipped: 0, errorsCount: 0 };

async function initPlayerWithRetry(maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const iframe = document.querySelector('iframe[src*="vimeo"]');
            if (!iframe) {
                throw new Error('Vimeo iframe not found');
            }
            
            const player = new window.Vimeo.Player(iframe);
            
            player.on('cuechange', function(data) {
                try {
                    if (transcriptData.length === 0 && data.cues.length > 0) {
                        console.log('=== Cue Object Structure ===');
                        console.log('Full cue object:', data.cues[0]);
                        console.log('Available properties:', Object.keys(data.cues[0]));
                        console.log('===========================');
                    }
                    
                    data.cues.forEach(async (cue) => {
                        try {
                            const startTime = cue.startTime || cue.start || await player.getCurrentTime();
                            const endTime = cue.endTime || cue.end || startTime + 3;
                            
                            const entry = { 
                                startTime: startTime,
                                endTime: endTime,
                                text: cue.text.trim() 
                            };
                            
                            if (!transcriptData.some(item => 
                                item.text === entry.text && 
                                Math.abs(item.startTime - entry.startTime) < 0.5)) {
                                transcriptData.push(entry);
                                processingStats.totalCues++;
                                console.log(`[${transcriptData.length}] ${startTime.toFixed(2)}s: ${cue.text}`);
                            } else {
                                processingStats.duplicatesSkipped++;
                            }
                        } catch (cueError) {
                            processingStats.errorsCount++;
                            console.warn('Cue processing error:', cueError);
                        }
                    });
                } catch (error) {
                    processingStats.errorsCount++;
                    console.error('Cuechange handler error:', error);
                }
            });
            
            window.vimeoPlayer = player;
            console.log(`Player initialized successfully (attempt ${i + 1})`);
            return;
        } catch (error) {
            console.warn(`Init attempt ${i + 1} failed:`, error);
            if (i === maxRetries - 1) {
                throw new Error(`Failed to initialize player after ${maxRetries} attempts: ${error.message}`);
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
}

async function startCaptionExtraction() {
    try {
        const player = window.vimeoPlayer;
        const duration = await player.getDuration();
        
        let originalVolume = 1;
        try {
            originalVolume = await player.getVolume();
            await player.setVolume(0);
            console.log('Audio muted (will restore after processing)');
            
            const startTime = Date.now();
            console.log(`Starting caption extraction for ${duration.toFixed(2)}s video`);
            
            for (let time = 0; time < duration; time += 1.5) {
                try {
                    await player.setCurrentTime(time);
                    await new Promise(resolve => setTimeout(resolve, 50));
                    
                    const progress = Math.round((time / duration) * 100);
                    if (progress % 10 === 0 && progress !== 0) {
                        const elapsed = Math.round((Date.now() - startTime) / 1000);
                        console.log(`Progress: ${progress}% (elapsed: ${elapsed}s, captions: ${transcriptData.length})`);
                    }
                } catch (seekError) {
                    console.warn(`Seek error at ${time}s:`, seekError);
                    processingStats.errorsCount++;
                    // Continue processing despite seek errors
                }
            }
            
            const totalTime = Math.round((Date.now() - startTime) / 1000);
            console.log('=== Extraction Completed ===');
            console.log(`Total captions: ${transcriptData.length}`);
            console.log(`Processing time: ${totalTime}s`);
            console.log(`Total cues processed: ${processingStats.totalCues}`);
            console.log(`Duplicates skipped: ${processingStats.duplicatesSkipped}`);
            console.log(`Errors encountered: ${processingStats.errorsCount}`);
            console.log('============================');
            
        } finally {
            await player.setVolume(originalVolume);
            console.log('Audio volume restored');
        }
    } catch (error) {
        console.error('Caption extraction failed:', error);
        throw error;
    }
}

// Initialize and start
initPlayerWithRetry().then(() => {
    console.log('Player ready. Starting caption extraction...');
    return startCaptionExtraction();
}).catch(error => {
    console.error('Process failed:', error);
});