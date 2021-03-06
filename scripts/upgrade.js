VERSION = 1.0

var hs = {
    meta: db.upgrade_meta_,
    
    dropIndexes: function(collection) {
        collection.dropIndexes();
    },
    
    convertDateField: function(collection, tfieldname, sfieldname) {
        var query = {};
        if (sfieldname === null || sfieldname === undefined)
            sfieldname = tfieldname;
        
        collection.find().snapshot().forEach(
            function(e) {
                var oldValue = e[sfieldname];
                query[tfieldname] = (
                    oldValue === null || oldValue === undefined
                        ? null
                        : new Date(oldValue.substr(0,23)));
                collection.update({_id: e._id}, {$set: query});
            }
        );
    },
    
    copyField: function(collection, ofieldname, nfieldname, transform) {
        var query = {};
        if (transform === null || transform === undefined) {
            transform = function(v) { return v; }
        }
        
        collection.find().snapshot().forEach(
            function(e) {
                if (ofieldname in e) {
                    query[nfieldname] = transform(e[ofieldname]);
                    collection.update({_id: e._id}, {$set: query});
                };
            }
        );
    },
    
    copyFields: function(collection, names, transform) {
        for (var i in names) {
            var fields = names[i];
            this.copyField(collection, fields[0], fields[1], transform);
        }
    },
    
    dropField: function(collection, fieldname) {
        var query = {};
        query[fieldname] = 1;
        collection.update({}, {$unset: query}, false, true);
    },
    
    dropFields: function(collection, fieldnames) {
        for (var i in fieldnames) {
            this.dropField(collection, fieldnames[i]);
        }
    },
    
    createField: function(collection, fieldname, defaultValue) {
        var query = {};
        collection.find().snapshot().forEach(
            function(e) {
                query[fieldname] = defaultValue;
                collection.update({_id: e._id}, {$set: query});
            }
        );
    },
    
    renameLastModifiedField: function(collection) {
        var tfieldname = 'last_updated'
          , sfieldname = 'last_modified';
        this.convertDateField(collection, tfieldname, sfieldname);
        this.dropField(collection, sfieldname);
    },
    
    updateSurveySchema: function(collection) {
        // create cin related fields
        collection.find().snapshot().forEach(
            function(e) {
                // create cin related fields
                var ss = e.rseq.substr(0, 6)
                  , up = e.rseq.substr(7, 1)
                  , cn = e.rseq.substr(9);
                
                collection.update({_id: e._id}, {$set: {
                    cin: ss + "/" + up + "/00/00/" + cn,
                    cin_station: ss,
                    cin_ltroute: up + "/00/00",
                    cin_custno: cn,
                    
                    // adjust project_id
                    project_id: e.project_id.substr(0, 4),
                }});
            }
        );
        
        // TODO: supplied find criteria
        // copy fields
        this.copyFields(collection, [
            ['kg_Id', 'kangis_no'],
            ['addy_no', 'addr_no'],
            ['addy_street', 'addr_street'],
            ['addy_town_city', 'addr_town'],
            ['addy_state', 'addr_state'],
            ['addy_lga', 'addr_lga'],
            ['addy_landmark', 'addr_landmark'],
            ['new_tholder', 'landlord_name'],
            ['tariff_new', 'tariff_pp']]);
        
        // TODO: supplied find criteria
        sleep(3000);
        this.dropFields(collection, [
            '_duration', '_submitted_by', '_status',
            'kg_Id', 'addy_no', 'addy_street', 'addy_town_city', 'addy_state',
            'addy_lga', 'addy_landmark', 'substation', 'new_tholder', 'tariff_new', 
            'last_payment', 'alt_power_source', 'uuid', 'acct_status_na_reason',
            'meter_status_other', 'meter_status_na_reason', 'meter_accessible',
            'meter_accessibility', 'meter_manuf_date', 'meter_cert_no', 'current_bill', 
            'outstanding_amt', 'bill_assessment', 'proposed_bill'
        ]);
    },
    
    updateXFormContent: function() {
        db.xforms.find().snapshot().forEach(
            function(e) {
                var formType = e.id_string[6] == 'f'? 'C': 'U';
                db.xforms.update({_id: e._id}, {$set: {type: formType}});
            }
        );
    },
    
    _doUpgrade: function(taskName, task) {
        // check if upgrade has been recorded
        var r = this.meta.findOne({task: taskName});
        if (r !== null && r !== undefined) {
            if (r.version >= VERSION && r.status === 'pass')
                return;
        }
        
        try {
            task();
            this.meta.update(
                {task: taskName},
                {$set: {status: 'pass', version: VERSION}},
                true
            );
            print('task : passed :: ' + taskName + '.');
        } catch (ex) {
            print('task : failed :: ' + taskName + '. \r\n' + ex);
            this.meta.remove({task: taskName});
        }
    },
    
    Upgrade: function() {
        var self = this;
        this._doUpgrade('drop-indexes', function() {
            self.dropIndexes(db.xforms);
            self.dropIndexes(db.projects);
            self.dropIndexes(db.stations);
        });
        
        this._doUpgrade('rename-last-modified-field', function(){
            self.renameLastModifiedField(db.projects);
            self.renameLastModifiedField(db.xforms);
            self.renameLastModifiedField(db.feeders);
            self.renameLastModifiedField(db.stations);
        });
        
        this._doUpgrade('convert-to-proper-date-fields', function() {
            self.convertDateField(db.xforms, 'date_created');
            self.convertDateField(db.captures, 'date_created');
            self.convertDateField(db.captures, 'last_updated');
            self.convertDateField(db.captures, '_submission_time');
            self.convertDateField(db.captures, 'datetime_today');
            self.convertDateField(db.captures, 'datetime_start');
            self.convertDateField(db.captures, 'datetime_end');
            
            self.convertDateField(db.updates, 'date_created');
            self.convertDateField(db.updates, 'last_updated');
            self.convertDateField(db.updates, '_submission_time');
            self.convertDateField(db.updates, 'datetime_today');
            self.convertDateField(db.updates, 'datetime_start');
            self.convertDateField(db.updates, 'datetime_end');
        });
        
        this._doUpgrade('update-project-schema', function(){
            var transform = function(value) {
                return value.substr(0, 4);
            }
            self.copyField(db.projects, 'id', 'code', transform);
            self.dropField(db.projects, 'id');
        });
        
        this._doUpgrade('update-xform-schema', function(){
            self.copyField(db.xforms, 'id', 'object_id');
            self.copyField(db.xforms, 'date_created', 'date_imported');
            sleep(3000);
            
            self.dropField(db.xforms, 'id');
            self.dropField(db.xforms, 'date_created');
        });
        
        this._doUpgrade('update-xform-content', self.updateXFormContent);
        
        this._doUpgrade('update-survey-schema', function() {
            self.updateSurveySchema(db.captures);
            self.updateSurveySchema(db.updates);
            self.dropField(db.updates, 'snapshots');
        });
    }
};