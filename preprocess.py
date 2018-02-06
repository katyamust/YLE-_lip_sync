import pandas as pd

video_features_df = pd.read_csv("saga_2min.mp4.csv")
#print(video_feaftures_df.shape)
#print(video_feaftures_df.head())

audio_features_df = pd.read_csv("saga_2min.wav.csv")
#print(audio_features_df.shape)
#print(audio_features_df.head())

# create sync dataset

# 1. merge video_and audio files
merge_df = video_features_df.merge(audio_features_df)
#print(merge_df.shape)

def concat_by_frame_25(merge_df):
    sync_df_list = [[]]
    for i in range(0,int(merge_df.shape[0]/25)):
        df_25 = merge_df.iloc[i*25:(i+1)*25]
        list_25 = list(df_25.values.flatten())
        sync_df_list.append(list_25)

    df_con = pd.DataFrame(sync_df_list)

    # print(df_con.shape)
    # print(df_con.head())

    return df_con

#2. roll out each 25 rows(one video frame) into one row
sync_dataset_df = concat_by_frame_25(merge_df)

#3. add  1 label
sync_dataset_df['sync'] = pd.Series(1, index=sync_dataset_df.index)

print("nonsync generate")
#print(audio_features_df.head())
# create (generate artificial) non sync dataset
shifted_audio_df = audio_features_df.iloc[4:]

shifted_audio_df["Index"] = shifted_audio_df['Index'].apply(lambda x : x-4)
#shifted_audio_df = shifted_audio_df.set_index("Index")
#shifted_audio_df = shifted_audio_df.reset_index();
#shifted_audio_df = shifted_audio_df.drop(columns=['Index'])
#shifted_audio_df = shifted_audio_df.drop(columns=['index'])
#video_features_df= video_features_df.reset_index(drop=True);

#video_features_df = video_features_df.drop(columns=['Index'])

#print(shifted_audio_df.shape)
#print(shifted_audio_df.head())
#print(video_features_df.shape)
#print(video_features_df.head())

merge_df_non_sync = video_features_df.merge(shifted_audio_df)
#print(merge_df_non_sync.shape)
#print(merge_df_non_sync.head())

non_sync_dataset_df = concat_by_frame_25(merge_df_non_sync)

#3. add 0 label
non_sync_dataset_df['sync'] = pd.Series(0, index=non_sync_dataset_df.index)

# generate artifitual non sync dataset
# shift audio features 4 frames forward

print("Summary")
print(non_sync_dataset_df.shape)
print(sync_dataset_df.shape)

print("Done")



