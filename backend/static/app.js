const fileElem = document.getElementById('fileElem');
const filePicker = document.getElementById('filePicker');
const dropArea = document.getElementById('drop-area');
const uploadBtn = document.getElementById('uploadBtn');
const status = document.getElementById('status');
const lengthSelect = document.getElementById('length');
const resultSection = document.getElementById('resultSection');
const summaryDiv = document.getElementById('summary');
const keypointsDiv = document.getElementById('keypoints');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');

let selectedFile = null;

filePicker.addEventListener('click', ()=> fileElem.click());
fileElem.addEventListener('change', (e)=> { selectedFile = e.target.files[0]; status.innerText = selectedFile ? selectedFile.name : ''; });

;['dragenter','dragover'].forEach(ev=>{
  dropArea.addEventListener(ev, (e)=>{ e.preventDefault(); dropArea.classList.add('hover'); });
});
;['dragleave','drop'].forEach(ev=>{
  dropArea.addEventListener(ev, (e)=>{ e.preventDefault(); dropArea.classList.remove('hover'); });
});
dropArea.addEventListener('drop', (e)=>{
  const dt = e.dataTransfer;
  const files = dt.files;
  if(files && files.length) {
    selectedFile = files[0];
    status.innerText = selectedFile.name;
  }
});

uploadBtn.addEventListener('click', async ()=>{
  if(!selectedFile){ status.innerText = 'Please choose a file first'; return; }
  resultSection.style.display = 'none';
  status.innerText = 'Uploading and processing...';
  uploadBtn.disabled = true;

  const form = new FormData();
  form.append('file', selectedFile);
  try {
    const res = await fetch('/api/upload', { method:'POST', body: form });
    const data = await res.json();
    if(!res.ok){ status.innerText = data.error || 'Processing failed'; uploadBtn.disabled = false; return; }
    const summaries = data.summaries || {};
    const len = lengthSelect.value || 'medium';
    const text = summaries[len] || summaries['medium'] || summaries['short'] || '';
    const kps = summaries['key_points'] || [];
    summaryDiv.innerText = text;
    if(kps.length){
      keypointsDiv.innerHTML = '<h3>Key Points</h3><ul>' + kps.map(k=>'<li>'+escapeHtml(k)+'</li>').join('') + '</ul>';
    } else {
      keypointsDiv.innerHTML = '';
    }
    resultSection.style.display = 'block';
    status.innerText = 'Done';
  } catch (err) {
    console.error(err);
    status.innerText = 'Upload failed';
  } finally {
    uploadBtn.disabled = false;
  }
});

copyBtn.addEventListener('click', async ()=>{
  const text = summaryDiv.innerText;
  if(!text) return;
  try {
    await navigator.clipboard.writeText(text);
    copyBtn.innerText = 'Copied!';
    setTimeout(()=> copyBtn.innerText = 'Copy', 1500);
  } catch (e) {
    alert('Copy failed');
  }
});

downloadBtn.addEventListener('click', ()=>{
  const text = summaryDiv.innerText;
  if(!text) return;
  const blob = new Blob([text], {type: 'text/plain'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'summary.txt';
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

function escapeHtml(unsafe) {
  return unsafe.replace(/[&<"'>]/g, function(m){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#039;"}[m]; });
}
