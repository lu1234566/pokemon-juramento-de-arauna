#include <mgba/flags.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mgba/core/core.h>
#include <mgba/core/config.h>
#include <mgba/core/log.h>
#include <mgba/gba/core.h>
#include <mgba-util/vfs.h>
#include <mgba/internal/arm/arm.h>
#include <mgba/internal/arm/isa-inlines.h>
static struct mCore*c;static color_t video[240*160];
static void quiet(struct mLogger*l,int a,enum mLogLevel b,const char*f,va_list v){}
static struct mLogger logger={.log=quiet};
int boot(const char*p){mLogSetDefaultLogger(&logger);c=GBACoreCreate();if(!c||!c->init(c))return 0;mCoreInitConfig(c,NULL);c->opts.useBios=0;c->opts.skipBios=1;c->setVideoBuffer(c,video,240);struct VFile*f=VFileOpen(p,O_RDONLY);if(!f||!c->loadROM(c,f))return 0;c->loadSave(c,VFileMemChunk(NULL,0));c->reset(c);return 1;}
void frames(uint32_t k,int n){c->setKeys(c,k);for(int i=0;i<n;i++)c->runFrame(c);}
uint32_t rd(uint32_t a,int n){return n==1?c->busRead8(c,a):n==2?c->busRead16(c,a):c->busRead32(c,a);}
void wr(uint32_t a,uint32_t v,int n){if(n==1)c->busWrite8(c,a,v);else if(n==2)c->busWrite16(c,a,v);else c->busWrite32(c,a,v);}
uint32_t pc(void){return ((struct ARMCore*)c->cpu)->gprs[ARM_PC];}
int invokex(uint32_t fn,uint32_t*args,uint32_t*out){struct ARMCore*cpu=c->cpu;int32_t regs[16];memcpy(regs,cpu->gprs,sizeof(regs));union PSR psr=cpu->cpsr;enum ExecutionMode mode=cpu->executionMode;uint32_t stack=cpu->gprs[ARM_SP],saved[4];for(int i=0;i<4;i++){saved[i]=rd(stack+4*i,4);wr(stack+4*i,args[4+i],4);}const uint32_t stop=0x09FFF000;uint32_t old=rd(stop,4);c->rawWrite16(c,stop,-1,0xE7FE);for(int i=0;i<4;i++)cpu->gprs[i]=args[i];cpu->gprs[ARM_LR]=stop|1;_ARMSetMode(cpu,MODE_THUMB);cpu->gprs[ARM_PC]=fn&~1;ThumbWritePC(cpu);int done=0;for(int i=0;i<80000000;i++){c->step(c);if((uint32_t)cpu->gprs[ARM_PC]==stop+2||(uint32_t)cpu->gprs[ARM_PC]==stop+4){done=1;break;}}*out=cpu->gprs[0];c->rawWrite32(c,stop,-1,old);memcpy(cpu->gprs,regs,sizeof(regs));for(int i=0;i<4;i++)wr(stack+4*i,saved[i],4);cpu->cpsr=psr;_ARMSetMode(cpu,mode);cpu->gprs[ARM_PC]-=mode==MODE_THUMB?2:4;if(mode==MODE_THUMB)ThumbWritePC(cpu);else ARMWritePC(cpu);return done;}
void pixels(const char*p){FILE*f=fopen(p,"wb");fwrite(video,sizeof(video),1,f);fclose(f);}

void shutdownx(void){if(c){c->deinit(c);c=NULL;}}
int exportsave(const char*p){void *b=NULL;size_t n=c->savedataClone(c,&b);if(!b||!n)return 0;FILE*f=fopen(p,"wb");if(!f){free(b);return 0;}size_t w=fwrite(b,1,n,f);fclose(f);free(b);return w==n;}
int importsave(const char*p){FILE*f=fopen(p,"rb");if(!f)return 0;fseek(f,0,SEEK_END);size_t n=ftell(f);rewind(f);void*b=malloc(n);size_t got=fread(b,1,n,f);fclose(f);int ok=got==n && c->loadSave(c,VFileMemChunk(b,n));free(b);c->reset(c);return ok;}
int statewrite(const char*p){size_t n=c->stateSize(c);void*b=malloc(n);int ok=c->saveState(c,b);if(ok){FILE*f=fopen(p,"wb");if(!f)ok=0;else{ok=fwrite(b,1,n,f)==n;fclose(f);}}free(b);return ok;}
int stateread(const char*p){size_t n=c->stateSize(c);void*b=malloc(n);FILE*f=fopen(p,"rb");if(!f){free(b);return 0;}int ok=fread(b,1,n,f)==n;fclose(f);if(ok)ok=c->loadState(c,b);free(b);return ok;}

#include <mgba/core/blip_buf.h>
int captureaudio(const char*p,int nf){FILE*f=fopen(p,"wb");if(!f)return 0;c->setAudioBufferSize(c,2048);blip_t*l=c->getAudioChannel(c,0),*r=c->getAudioChannel(c,1);blip_set_rates(l,c->frequency(c),24000);blip_set_rates(r,c->frequency(c),24000);blip_clear(l);blip_clear(r);int total=0;for(int i=0;i<nf;i++){c->runFrame(c);int n=blip_samples_avail(l),nr=blip_samples_avail(r);if(nr<n)n=nr;if(n>2048)n=2048;short samples[4096];blip_read_samples(l,samples,n,1);blip_read_samples(r,samples+1,n,1);fwrite(samples,sizeof(short)*2,n,f);total+=n;}fclose(f);return total;}
