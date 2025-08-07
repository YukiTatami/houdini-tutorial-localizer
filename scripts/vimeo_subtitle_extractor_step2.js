// Vimeo字幕取得スクリプト - ステップ2: SRT形式変換
// 使用方法: ステップ1実行後、続けてこのコードを実行

function formatTime(seconds) {
    var h = Math.floor(seconds / 3600);
    var m = Math.floor((seconds % 3600) / 60);
    var s = Math.floor(seconds % 60);
    var ms = Math.floor((seconds % 1) * 1000);
    return h.toString().padStart(2, '0') + ':' + m.toString().padStart(2, '0') + ':' + s.toString().padStart(2, '0') + ',' + ms.toString().padStart(3, '0');
}

function convertToSRT() {
    try {
        if (transcriptData.length === 0) {
            console.error('No transcript data available. Please run caption extraction first.');
            return;
        }
        
        var srtContent = '';
        var sortedData = transcriptData.sort(function(a, b) { return a.startTime - b.startTime; });
        
        // Remove duplicates and validate data
        var cleanedData = [];
        var lastEntry = null;
        
        for (var i = 0; i < sortedData.length; i++) {
            var item = sortedData[i];
            
            // Validate entry
            if (!item.text || item.text.trim() === '') continue;
            if (item.startTime < 0 || item.endTime <= item.startTime) continue;
            
            // Check for duplicates
            if (lastEntry && 
                lastEntry.text === item.text && 
                Math.abs(lastEntry.startTime - item.startTime) < 1.0) {
                continue;
            }
            
            cleanedData.push(item);
            lastEntry = item;
        }
        
        console.log(`Data cleaning: ${sortedData.length} → ${cleanedData.length} entries`);
        
        for (var i = 0; i < cleanedData.length; i++) {
            var item = cleanedData[i];
            var startTime = formatTime(item.startTime);
            var endTime = formatTime(item.endTime);
            srtContent += (i + 1) + '\n';
            srtContent += startTime + ' --> ' + endTime + '\n';
            srtContent += item.text + '\n\n';
        }
        
        console.log('=== SRT Conversion Statistics ===');
        console.log('Original entries:', transcriptData.length);
        console.log('Cleaned entries:', cleanedData.length);
        console.log('Duplicates removed:', transcriptData.length - cleanedData.length);
        console.log('Total video duration:', cleanedData.length > 0 ? formatTime(cleanedData[cleanedData.length-1].endTime) : 'N/A');
        console.log('IMPORTANT: Save file as UTF-8 encoding');
        console.log('================================');
        console.log('===== COPY THE TEXT BELOW =====');
        console.log(srtContent);
        console.log('===== END OF SRT DATA =====');
        
        return srtContent;
    } catch (error) {
        console.error('SRT conversion failed:', error);
        return null;
    }
}

convertToSRT();