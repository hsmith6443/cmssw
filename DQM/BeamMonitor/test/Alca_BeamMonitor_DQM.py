import FWCore.ParameterSet.Config as cms

process = cms.Process("DQM")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'/store/relval/CMSSW_3_8_0/MinimumBias/ALCARECO/GR_R_38X_V7_RelVal_col_10_bs_TkAlMinBias-v1/0007/90B6F8D6-4E96-DF11-B3A9-0018F3D0970A.root',
#'/store/relval/CMSSW_3_8_0/MinimumBias/ALCARECO/GR_R_38X_V7_RelVal_col_10_bs_TkAlMinBias-v1/0007/8A6CDD40-C995-DF11-B6D5-0018F3D096AA.root'
    )
#    , duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

# initialize MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.categories = ["AlcaBeamMonitor"]
process.MessageLogger.cerr = cms.untracked.PSet(placeholder = cms.untracked.bool(True))
process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string('INFO'),
    default = cms.untracked.PSet(
       limit = cms.untracked.int32(0)
    ),
    AlcaBeamMonitor = cms.untracked.PSet(
        #reportEvery = cms.untracked.int32(100) # every 1000th only
	limit = cms.untracked.int32(0)
    )
)
#process.MessageLogger.statistics.append('cout')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load("DQMServices.Core.DQM_cfg")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.EventContent.EventContent_cff')

process.load("DQM.BeamMonitor.AlcaBeamMonitor_cff")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.BeamSpotDBSource = cms.ESSource("PoolDBESSource",
                                        process.CondDBSetup,
                                        toGet = cms.VPSet(cms.PSet(
    								   record = cms.string('BeamSpotObjectsRcd'),			        
#    								   tag = cms.string('BeamSpotObjects_2009_LumiBased_v16_offline') 
    								   tag = cms.string('BeamSpotObject_ByLumi') 
    								  )
						         ),								        
                                         #connect = cms.string('frontier://cmsfrontier.cern.ch:8000/Frontier/CMS_COND_31X_BEAMSPOT')
                                         connect = cms.string('sqlite_file:step4.db')
                                         #connect = cms.string('oracle://cms_orcoff_prod/CMS_COND_31X_BEAMSPOT')
                                         #connect = cms.string('frontier://PromptProd/CMS_COND_31X_BEAMSPOT')
                                        )


process.DQMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = process.DQMEventContent.outputCommands,
    fileName = cms.untracked.string('step5_DQM.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    )
)
process.DQMoutput.outputCommands.append('drop *')
process.DQMoutput.outputCommands.append('keep *_MEtoEDMConverter_*_*')

# # summary
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )

process.pp = cms.Path(process.AlcaBeamMonitor*process.endOfProcess*process.DQMoutput)
process.schedule = cms.Schedule(process.pp)
